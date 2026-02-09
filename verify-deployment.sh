#!/bin/bash

# Verification script for know.crpg.info deployment
# Tests all 92 atomic articles for accessibility

BASE_URL="https://know.crpg.info"
CONTENT_DIR="content"
PASS_COUNT=0
FAIL_COUNT=0
REDIRECT_COUNT=0

echo "========================================="
echo "Deployment Verification for know.crpg.info"
echo "========================================="
echo ""
echo "Testing all markdown files for HTTP 200 OK..."
echo ""

# Create results file
RESULTS_FILE="verification-results.txt"
echo "Verification Results - $(date)" > "$RESULTS_FILE"
echo "=========================================" >> "$RESULTS_FILE"
echo "" >> "$RESULTS_FILE"

# Find all markdown files and test them
while IFS= read -r file; do
    # Remove ./ prefix and .md extension
    clean_path="${file#./}"
    clean_path="${clean_path%.md}"

    # Skip index.md in root (test separately)
    if [ "$clean_path" = "index" ]; then
        url="$BASE_URL/"
    else
        url="$BASE_URL/$clean_path"
    fi

    # Get HTTP status code
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")

    if [ "$status" = "200" ]; then
        echo "✓ $clean_path (HTTP $status)"
        echo "✓ $url (HTTP $status)" >> "$RESULTS_FILE"
        ((PASS_COUNT++))
    elif [ "$status" = "301" ] || [ "$status" = "302" ]; then
        echo "↻ $clean_path (HTTP $status - redirect)"
        echo "↻ $url (HTTP $status)" >> "$RESULTS_FILE"
        ((REDIRECT_COUNT++))
    else
        echo "✗ $clean_path (HTTP $status - FAILED)"
        echo "✗ $url (HTTP $status - FAILED)" >> "$RESULTS_FILE"
        ((FAIL_COUNT++))
    fi
done < <(cd "$CONTENT_DIR" && find . -name "*.md" -type f | sort)

echo ""
echo "========================================="
echo "Verification Summary"
echo "========================================="
echo "✓ Passed (HTTP 200):      $PASS_COUNT"
echo "↻ Redirects (HTTP 3xx):   $REDIRECT_COUNT"
echo "✗ Failed (Non-200):       $FAIL_COUNT"
echo "========================================="
echo "Total files tested:       $((PASS_COUNT + REDIRECT_COUNT + FAIL_COUNT))"
echo ""

# Add summary to results file
echo "" >> "$RESULTS_FILE"
echo "=========================================" >> "$RESULTS_FILE"
echo "Summary:" >> "$RESULTS_FILE"
echo "Passed: $PASS_COUNT" >> "$RESULTS_FILE"
echo "Redirects: $REDIRECT_COUNT" >> "$RESULTS_FILE"
echo "Failed: $FAIL_COUNT" >> "$RESULTS_FILE"
echo "Total: $((PASS_COUNT + REDIRECT_COUNT + FAIL_COUNT))" >> "$RESULTS_FILE"

echo "Full results saved to: $RESULTS_FILE"
echo ""

# Exit with error if any failures
if [ $FAIL_COUNT -gt 0 ]; then
    exit 1
else
    echo "✓ All pages are accessible!"
    exit 0
fi
