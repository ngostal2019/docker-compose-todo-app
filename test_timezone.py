#!/usr/bin/env python3
"""Test dynamic timezone functionality"""
import requests
from datetime import datetime

# Create a session to maintain cookies
session = requests.Session()
BASE_URL = "http://localhost:5000"

print("=" * 60)
print("Testing Dynamic Timezone Feature")
print("=" * 60)

# Step 1: Visit homepage to initialize session
print("\n1. Initializing session...")
resp = session.get(f"{BASE_URL}/")
print(f"   Status: {resp.status_code}")

# Step 2: Check initial timezone (should be UTC)
print("\n2. Checking initial timezone...")
resp = session.get(f"{BASE_URL}/settings")
if "UTC" in resp.text:
    print("   ✓ Initial timezone is UTC")

# Step 3: Update timezone to America/Chicago
print("\n3. Updating timezone to America/Chicago...")
resp = session.post(f"{BASE_URL}/settings", data={"timezone": "America/Chicago"})
if "Timezone updated" in resp.text:
    print("   ✓ Timezone updated successfully")
else:
    print("   Response status:", resp.status_code)
    print("   Response contains 'America/Chicago':", "America/Chicago" in resp.text)

# Step 4: Verify timezone was saved
print("\n4. Verifying timezone was saved...")
resp = session.get(f"{BASE_URL}/settings")
if "America/Chicago" in resp.text and '<strong>America/Chicago</strong>' in resp.text:
    print("   ✓ Timezone saved as America/Chicago")
else:
    print("   ✗ Timezone not saved correctly")
    print("   Response:", resp.text[1000:1500])

# Step 5: Create a todo
print("\n5. Creating a new todo...")
resp = session.post(f"{BASE_URL}/create", data={
    "title": "Test Dynamic Timezone",
    "description": "Testing user timezone conversion"
})
if resp.status_code in [200, 302]:
    print("   ✓ Todo created successfully")

# Step 6: Check todo displays with correct timezone
print("\n6. Checking todo timestamps with America/Chicago timezone...")
resp = session.get(f"{BASE_URL}/")
if "CST" in resp.text or "Chicago" in resp.text or "America/Chicago" in resp.text:
    print("   ✓ Timezone indicator visible on todo")
    # Extract created timestamp
    if "Created:" in resp.text:
        start = resp.text.find("Created: ") + 9
        end = resp.text.find("</span>", start)
        timestamp = resp.text[start:end]
        print(f"   Todo timestamp: {timestamp}")

# Step 7: Show current settings summary
print("\n7. Current User Settings:")
resp = session.get(f"{BASE_URL}/settings")
if '<strong>America/Chicago</strong>' in resp.text:
    print("   ✓ Timezone: America/Chicago")
    print("   ✓ All todos will display in CST (Central Standard Time)")

print("\n" + "=" * 60)
print("Dynamic Timezone Test Complete!")
print("=" * 60)
