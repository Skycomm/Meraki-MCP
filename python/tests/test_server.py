"""
Tests for Meraki MCP Server
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import time

from meraki_mcp.server import (
    MerakiClient,
    check_rate_limit,
    format_response,
    check_privileges,
    list_organizations,
    get_uplink_loss_latency,
    reboot_device
)
from mcp.types import TextContent


@pytest.fixture
def mock_meraki_client():
    """Mock Meraki client for testing"""
    client = AsyncMock(spec=MerakiClient)
    return client


@pytest.fixture
def mock_context():
    """Mock MCP context"""
    context = Mock()
    context.meta = {"user_id": "test_user"}
    return context


class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_rate_limit_allows_initial_requests(self):
        """Test that rate limiting allows initial requests"""
        user_id = "test_user_1"
        assert check_rate_limit(user_id) is True
    
    def test_rate_limit_blocks_excessive_requests(self):
        """Test that rate limiting blocks excessive requests"""
        user_id = "test_user_2"
        
        # Make requests up to the limit
        for _ in range(100):
            assert check_rate_limit(user_id) is True
        
        # Next request should be blocked
        assert check_rate_limit(user_id) is False
    
    def test_rate_limit_resets_after_window(self):
        """Test that rate limit resets after time window"""
        user_id = "test_user_3"
        
        # Fill up the rate limit
        for _ in range(100):
            check_rate_limit(user_id)
        
        # Should be blocked
        assert check_rate_limit(user_id) is False
        
        # Mock time passing
        with patch('time.time', return_value=time.time() + 61):
            # Should be allowed again
            assert check_rate_limit(user_id) is True


class TestAuthentication:
    """Test authentication and authorization"""
    
    def test_check_privileges_allows_privileged_users(self):
        """Test that privileged users are allowed"""
        context = Mock()
        context.meta = {"user_id": "admin@example.com"}
        
        with patch('meraki_mcp.server.PRIVILEGED_USERS', ["admin@example.com"]):
            assert check_privileges(context, "reboot_device") is True
    
    def test_check_privileges_denies_unprivileged_users(self):
        """Test that unprivileged users are denied"""
        context = Mock()
        context.meta = {"user_id": "regular_user"}
        
        with patch('meraki_mcp.server.PRIVILEGED_USERS', ["admin@example.com"]):
            assert check_privileges(context, "reboot_device") is False


class TestResponseFormatting:
    """Test response formatting"""
    
    def test_format_response_success(self):
        """Test formatting successful responses"""
        response = format_response("Success message", success=True)
        
        assert len(response) == 1
        assert isinstance(response[0], TextContent)
        assert response[0].text == "Success message"
    
    def test_format_response_error(self):
        """Test formatting error responses"""
        response = format_response("Error message", success=False)
        
        assert len(response) == 1
        assert isinstance(response[0], TextContent)
        assert response[0].text == "Error message"


@pytest.mark.asyncio
class TestTools:
    """Test MCP tools"""
    
    async def test_list_organizations_success(self, mock_context, mock_meraki_client):
        """Test successful organization listing"""
        # Mock API response
        mock_orgs = [
            {"id": "123", "name": "Test Org", "url": "https://test.com", "api": {"enabled": True}}
        ]
        mock_meraki_client.get.return_value = mock_orgs
        
        with patch('meraki_mcp.server.meraki_client', mock_meraki_client):
            result = await list_organizations(mock_context)
        
        assert len(result) == 1
        assert "Test Org" in result[0].text
        assert "123" in result[0].text
    
    async def test_list_organizations_rate_limit(self, mock_context):
        """Test rate limiting on organization listing"""
        # Fill up rate limit
        with patch('meraki_mcp.server.RATE_LIMIT_REQUESTS', 1):
            check_rate_limit("test_user")  # Use up the limit
            
            result = await list_organizations(mock_context)
            
            assert len(result) == 1
            assert "Rate limit exceeded" in result[0].text
    
    async def test_reboot_device_requires_privileges(self, mock_context):
        """Test that reboot requires privileges"""
        with patch('meraki_mcp.server.PRIVILEGED_USERS', []):
            result = await reboot_device(
                mock_context,
                serial="Q2XX-XXXX",
                confirmation="YES-REBOOT-Q2XX-XXXX"
            )
            
            assert len(result) == 1
            assert "Access Denied" in result[0].text
    
    async def test_reboot_device_requires_confirmation(self, mock_context):
        """Test that reboot requires proper confirmation"""
        mock_context.meta = {"user_id": "admin@example.com"}
        
        with patch('meraki_mcp.server.PRIVILEGED_USERS', ["admin@example.com"]):
            result = await reboot_device(
                mock_context,
                serial="Q2XX-XXXX",
                confirmation="wrong-confirmation"
            )
            
            assert len(result) == 1
            assert "CONFIRMATION REQUIRED" in result[0].text
    
    async def test_uplink_loss_latency_alerts(self, mock_context, mock_meraki_client):
        """Test uplink loss/latency with alerts"""
        # Mock API response with high loss
        mock_data = [{
            "serial": "Q2XX-XXXX",
            "uplink": "wan1",
            "ip": "1.2.3.4",
            "timeSeries": [
                {"lossPercent": 5.0, "latencyMs": 150.0},
                {"lossPercent": 3.0, "latencyMs": 120.0}
            ]
        }]
        mock_meraki_client.get.return_value = mock_data
        
        with patch('meraki_mcp.server.meraki_client', mock_meraki_client):
            result = await get_uplink_loss_latency(mock_context, org_id="123")
        
        assert len(result) == 1
        text = result[0].text
        assert "Alerts" in text  # Should have alerts section
        assert "Average packet loss" in text  # Should warn about loss


@pytest.mark.asyncio
class TestMerakiClient:
    """Test Meraki API client"""
    
    async def test_client_get_request(self):
        """Test GET request handling"""
        with patch('httpx.AsyncClient.get') as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status = Mock()
            mock_response.json.return_value = {"test": "data"}
            mock_get.return_value = mock_response
            
            client = MerakiClient("test-key")
            result = await client.get("/test")
            
            assert result == {"test": "data"}
            mock_get.assert_called_once()
    
    async def test_client_error_handling(self):
        """Test error handling in client"""
        with patch('httpx.AsyncClient.get') as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = Exception("API Error")
            mock_get.return_value = mock_response
            
            client = MerakiClient("test-key")
            
            with pytest.raises(Exception) as exc_info:
                await client.get("/test")
            
            assert "API Error" in str(exc_info.value)