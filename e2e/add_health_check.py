# Add a simple test to the existing health endpoint or create a debug endpoint
with open('app/main.py', 'r') as f:
    content = f.read()

# Add a debug endpoint after health
health_end = content.find('@app.get("/debug/swe-test")')
if health_end == -1:
    health_end = len(content)

debug_endpoint = '''

@app.get("/debug/cors-test")
def cors_test():
    """Test endpoint for CORS."""
    return {"message": "CORS test"}

@app.delete("/debug/delete-test")
def delete_test():
    """Test DELETE without auth."""
    return {"message": "DELETE test"}

'''

content = content[:health_end] + debug_endpoint + content[health_end:]

with open('app/main.py', 'w') as f:
    f.write(content)

print("Added debug endpoints")
