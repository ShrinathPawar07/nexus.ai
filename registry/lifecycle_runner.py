# lifecycle_runner.py

def run_hook(plugin, hook_name):
    hook = plugin.get("lifecycle_hooks", {}).get(hook_name)
    if callable(hook):
        try:
            hook()
        except Exception as e:
            print(f"[Lifecycle Error] {hook_name} failed: {e}")