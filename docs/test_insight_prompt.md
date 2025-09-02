# Insight Tools Test Prompt (Read-Only)

Please run a comprehensive test of the Insight monitoring tools for the Skycomm organization. This is a READ-ONLY test - do not create, update, or delete anything.

## Test the following Insight tools:

### 1. Organization-Level Insight Tools:
- List all monitored media servers for Skycomm (org ID: 686470)
- List all monitored applications for Skycomm
- If any media servers exist, get details for one of them

### 2. Network-Level Application Health:
- For the Reserve St network (ID: L_726205439913500692), try to get application health metrics
- Use common application IDs like:
  - "meraki:insight:0" (WebEx)
  - "meraki:insight:1" (Zoom)  
  - "meraki:insight:2" (Microsoft Teams)
- Use a 24-hour timespan with 3600-second resolution

### 3. Expected Results:
- Some tools may return empty results if Insight is not licensed
- Tools should handle licensing errors gracefully
- All tools should format output clearly even with no data

### 4. Error Handling:
- Note any tools that fail with errors
- Check if error messages mention licensing requirements
- Verify all tools return helpful messages even when no data exists

## Important Notes:
- This is READ-ONLY - do not use any create/update/delete tools
- If you see "license required" errors, that's expected and OK
- Focus on verifying the tools work and handle errors properly

Please provide a summary of:
1. Which tools worked successfully
2. Which tools require licensing
3. Any unexpected errors
4. Overall assessment of Insight tools functionality