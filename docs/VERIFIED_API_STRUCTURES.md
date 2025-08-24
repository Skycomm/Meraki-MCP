# ✅ Verified Meraki API Data Structures

This document contains the ACTUAL, VERIFIED data structures returned by Meraki APIs.

## 1. Organization APIs

### get_organizations()
- **Returns**: `List[Dict]`
- **Structure**:
```python
[
  {
    "id": "686470",
    "name": "Skycomm",
    "url": "https://...",
    "api": {"enabled": true},
    "licensing": {...},
    "cloud": {...},
    "management": {...}
  }
]
```

### get_organization(org_id)
- **Returns**: `Dict`
- **Structure**: Same as single org entry above

## 2. Device APIs

### get_organization_devices(org_id)
- **Returns**: `List[Dict]`
- **Structure**:
```python
[
  {
    "name": "Device Name",
    "serial": "Q2HP-XXXX-XXXX",
    "mac": "00:00:00:00:00:00",
    "networkId": "L_xxx",
    "model": "MS220-8P",
    "firmware": "version",
    "lanIp": "192.168.1.1"
  }
]
```

## 3. Analytics APIs (CRITICAL)

### get_organization_devices_uplinks_loss_and_latency(org_id, timespan)
- **Returns**: `List[Dict]` - FLAT LIST (one entry per uplink)
- **Max timespan**: 300 seconds (5 minutes)
- **Structure**:
```python
[
  {
    "networkId": "L_xxx",
    "serial": "Q2MN-XXXX-XXXX",
    "uplink": "wan1",  # or "wan2"
    "ip": "144.139.213.111",
    "timeSeries": [
      {
        "ts": "2025-08-17T13:47:29Z",
        "lossPercent": 0.0,
        "latencyMs": 45.2
      }
    ]
  }
]
```
**NOTE**: Each uplink is a separate entry in the list!

### get_network_appliance_uplinks_usage_history(network_id, timespan)
- **Returns**: `List[Dict]`
- **Structure**:
```python
[
  {
    "startTime": "2025-08-17T12:53:00Z",
    "endTime": "2025-08-17T12:54:00Z",
    "byInterface": [  # This is a LIST, not dict!
      {
        "interface": "wan1",
        "sent": 314941,      # bytes
        "received": 431119   # bytes
      }
    ]
  }
]
```
**NOTE**: `byInterface` is a LIST of interfaces!

### get_network_connection_stats(network_id, timespan)
- **Returns**: `Dict` (single summary) or `List[Dict]` (time series)
- **Single summary structure**:
```python
{
  "assoc": 100,    # Total associations
  "auth": 95,      # Successful auth
  "dhcp": 94,      # DHCP success
  "dns": 93,       # DNS success
  "success": 90    # Overall success
}
```

### get_network_latency_stats(network_id, timespan)
- **Returns**: `Dict` with backgroundTraffic
- **Structure**:
```python
{
  "backgroundTraffic": {
    "rawDistribution": {
      "0-5ms": 100,
      "5-10ms": 50,
      // etc
    }
  }
}
```

## 4. Live Tools APIs (Beta)

### create_device_live_tools_ping(serial, target, count)
- **Returns**: `Dict`
- **Max count**: 5
- **Structure**:
```python
{
  "pingId": "669347494714228788",
  "url": "/devices/XXX/liveTools/ping/XXX",
  "request": {
    "serial": "Q2MN-XXXX-XXXX",
    "target": "8.8.8.8",
    "count": 5
  },
  "status": "new"
}
```

### get_device_live_tools_ping(serial, ping_id)
- **Returns**: `Dict`
- **Structure**:
```python
{
  "pingId": "xxx",
  "status": "complete",
  "results": {
    "sent": 5,
    "received": 5,
    "loss": {"percentage": 0.0},  # Nested object!
    "latencies": {...},
    "replies": [...]
  }
}
```

## 5. Performance APIs

### get_device_appliance_performance(serial)
- **Returns**: `Dict`
- **Structure**:
```python
{
  "perfScore": 8.0  # Simple score, not detailed metrics
}
```

## Key Parsing Fixes Needed:

1. ✅ **Connection Stats**: Handle both dict and list responses
2. ✅ **Uplink Usage History**: `byInterface` is a LIST, not dict
3. ✅ **Loss/Latency**: Flat list with one entry per uplink
4. ✅ **Ping Results**: Loss is nested as `results.loss.percentage`

## API Limitations:

1. **Packet Loss History**: Only 5 minutes available via API (dashboard stores 24h)
2. **Performance Details**: Only returns simple score, not CPU/memory
3. **Latency History**: No historical data beyond 5 minutes
4. **Connection Stats**: May return summary or time series

## Working Examples:

```python
# Get current packet loss (5 min window)
loss_data = meraki.get_organization_devices_uplinks_loss_and_latency(org_id, 300)
for uplink in loss_data:
    if uplink['serial'] == target_serial and uplink['uplink'] == 'wan1':
        latest = uplink['timeSeries'][-1]
        print(f"Loss: {latest['lossPercent']}%")

# Get traffic usage (24 hours available)
history = meraki.get_network_appliance_uplinks_usage_history(network_id, 86400)
for entry in history:
    for iface in entry['byInterface']:
        if iface['interface'] == 'wan1':
            total_kb = (iface['sent'] + iface['received']) / 1024
            print(f"{entry['startTime']}: {total_kb} KB")
```