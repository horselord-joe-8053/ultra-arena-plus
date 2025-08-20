#!/bin/bash

# 🚀 Simple Ultra Arena API Test - Health Check
# Just checks if the server is running!

BASE_URL="http://localhost:5002"
ENDPOINT="/api/health"
FULL_URL="${BASE_URL}${ENDPOINT}"

echo "🚀 Starting Health Check..."
echo "📍 Testing: $FULL_URL"
echo ""

echo "📤 Sending GET request..."
echo ""

response=$(curl -s -w "\n%{http_code}" -X GET "${FULL_URL}")

http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | sed '$d')

echo "📥 Response received!"
echo "🔢 Status Code: $http_code"
echo "📄 Response:"
echo "$response_body" | python3 -m json.tool 2>/dev/null || echo "$response_body"
echo ""

if [ "$http_code" -eq 200 ]; then
    echo "✅ SUCCESS! Server is healthy!"
else
    echo "❌ FAILED! Server might be down!"
fi

echo ""
echo "🎉 Health check completed!" 