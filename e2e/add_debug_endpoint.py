import sys
sys.path.insert(0, '/Users/meharban/Projects/Autonmous_Factory/multi_llm_orchestrator/case-studies/project_28_astro_app')

# Read the kundli.py file and add debug logging
with open('app/routes/kundli.py', 'r') as f:
    content = f.read()

# Add import for traceback at the top if not present
if 'import traceback' not in content:
    content = content.replace(
        'from app.kp_engine import calculate_kp_cuspal',
        'from app.kp_engine import calculate_kp_cuspal\nimport traceback'
    )

# Update delete_all_my_kundlis to have detailed error logging
to_replace = '''@router.delete("/user/all", status_code=status.HTTP_200_OK)
async def delete_all_my_kundlis(
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete all kundlis for the current user."""
    try:'''

new_content = '''@router.delete("/user/all", status_code=status.HTTP_200_OK)
async def delete_all_my_kundlis(
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete all kundlis for the current user."""
    print(f"DEBUG: delete_all_my_kundlis called")
    print(f"DEBUG: current_user = {current_user}")
    try:'''

content = content.replace(to_replace, new_content)

with open('app/routes/kundli.py', 'w') as f:
    f.write(content)

print("Updated kundli.py with debug logging")
