#!/usr/bin/env python3
"""
CLI wrapper for Meraki MCP Server
Provides a simple command-line interface for common operations
"""

import asyncio
import os
import sys
from typing import Optional
import click
import json

from .server import MerakiClient, init_server, meraki_client


@click.group()
@click.option('--api-key', envvar='MERAKI_API_KEY', help='Meraki API key')
@click.pass_context
def cli(ctx, api_key):
    """Meraki MCP Server CLI - Direct access to Meraki tools"""
    if not api_key:
        click.echo("Error: MERAKI_API_KEY not set", err=True)
        sys.exit(1)
    
    ctx.ensure_object(dict)
    ctx.obj['api_key'] = api_key


@cli.command()
@click.pass_context
def list_orgs(ctx):
    """List all organizations"""
    async def run():
        client = MerakiClient(ctx.obj['api_key'])
        try:
            orgs = await client.get("/organizations")
            for org in orgs:
                click.echo(f"{org['id']}: {org['name']}")
        finally:
            await client.close()
    
    asyncio.run(run())


@cli.command()
@click.argument('org_id')
@click.pass_context
def list_networks(ctx, org_id):
    """List networks in an organization"""
    async def run():
        client = MerakiClient(ctx.obj['api_key'])
        try:
            networks = await client.get(f"/organizations/{org_id}/networks")
            for net in networks:
                types = ', '.join(net.get('productTypes', ['Unknown']))
                click.echo(f"{net['id']}: {net['name']} ({types})")
        finally:
            await client.close()
    
    asyncio.run(run())


@cli.command()
@click.argument('org_id')
@click.option('--timespan', default=300, help='Timespan in seconds (max 300)')
@click.option('--json-output', is_flag=True, help='Output as JSON')
@click.pass_context
def check_uplinks(ctx, org_id, timespan, json_output):
    """Check uplink packet loss and latency"""
    async def run():
        client = MerakiClient(ctx.obj['api_key'])
        try:
            data = await client.get(
                f"/organizations/{org_id}/devices/uplinks/lossAndLatency?timespan={timespan}",
                use_cache=False
            )
            
            if json_output:
                click.echo(json.dumps(data, indent=2))
                return
            
            # Process and display alerts
            alerts = []
            for entry in data:
                serial = entry.get('serial', 'Unknown')
                uplink = entry.get('uplink', 'Unknown')
                time_series = entry.get('timeSeries', [])
                
                if time_series:
                    # Calculate average loss
                    losses = [p.get('lossPercent', 0) for p in time_series if p.get('lossPercent') is not None]
                    if losses:
                        avg_loss = sum(losses) / len(losses)
                        if avg_loss > 1:
                            alerts.append(f"⚠️  {serial} {uplink}: {avg_loss:.1f}% average loss")
            
            if alerts:
                click.echo("ALERTS FOUND:")
                for alert in alerts:
                    click.echo(alert)
            else:
                click.echo("✅ All uplinks healthy")
                
        finally:
            await client.close()
    
    asyncio.run(run())


@cli.command()
@click.argument('serial')
@click.argument('target')
@click.option('--count', default=5, help='Number of pings (max 5)')
@click.pass_context
def ping(ctx, serial, target, count):
    """Run a ping test from a device"""
    async def run():
        client = MerakiClient(ctx.obj['api_key'])
        try:
            result = await client.post(
                f"/devices/{serial}/liveTools/ping",
                {"target": target, "count": min(count, 5)}
            )
            
            job_id = result.get('pingId') or result.get('id')
            if job_id:
                click.echo(f"✅ Ping test started")
                click.echo(f"Job ID: {job_id}")
                click.echo(f"Device: {serial}")
                click.echo(f"Target: {target}")
                click.echo(f"\nTo check results:")
                click.echo(f"meraki-cli ping-results {serial} {job_id}")
            else:
                click.echo("❌ Failed to start ping test", err=True)
                
        finally:
            await client.close()
    
    asyncio.run(run())


@cli.command()
@click.argument('serial')
@click.argument('ping_id')
@click.pass_context
def ping_results(ctx, serial, ping_id):
    """Get ping test results"""
    async def run():
        client = MerakiClient(ctx.obj['api_key'])
        try:
            result = await client.get(f"/devices/{serial}/liveTools/ping/{ping_id}")
            
            click.echo(f"Status: {result.get('status', 'Unknown')}")
            
            results = result.get('results', {})
            if results:
                loss = results.get('loss', {}).get('percentage', 0)
                sent = results.get('sent', 0)
                received = results.get('received', 0)
                
                click.echo(f"\nResults:")
                click.echo(f"  Sent: {sent}")
                click.echo(f"  Received: {received}")
                click.echo(f"  Loss: {loss}%")
                
                latencies = results.get('latencies', {})
                if latencies:
                    click.echo(f"\nLatency:")
                    click.echo(f"  Min: {latencies.get('minimum', 0)}ms")
                    click.echo(f"  Avg: {latencies.get('average', 0)}ms")
                    click.echo(f"  Max: {latencies.get('maximum', 0)}ms")
                    
        finally:
            await client.close()
    
    asyncio.run(run())


@cli.command()
@click.pass_context
def serve(ctx):
    """Start the MCP server (for use with Claude)"""
    click.echo("Starting Meraki MCP server...")
    from .server import main
    asyncio.run(main())


if __name__ == "__main__":
    cli()