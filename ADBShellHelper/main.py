import subprocess
import time
import re

# List of keywords commonly found in adware/junk apps
SUSPICIOUS_KEYWORDS = [
    "clean",
    "booster",
    "game",
    "speed",
    "security",
    "junk",
    "master",
]


def run_adb(command):
    """Run an ADB command and return output."""
    try:
        result = subprocess.run(
            ["adb"] + command.split(), capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"


def list_user_apps():
    """List all user-installed apps, highlight suspicious ones."""
    output = run_adb("shell pm list packages -3")
    packages = [line.replace("package:", "") for line in output.splitlines()]

    print("\nUser-installed apps:")
    for pkg in packages:
        if any(keyword.lower() in pkg.lower() for keyword in SUSPICIOUS_KEYWORDS):
            print(f"[!] {pkg}  <-- Suspicious")
        else:
            print(pkg)
    return packages


def uninstall_app(packages=None):
    """Prompt the user to uninstall an app."""
    if not packages:
        packages = list_user_apps()
    pkg = input("\nEnter package name to uninstall: ").strip()
    if pkg not in packages:
        print("Package not found among user-installed apps!")
        return
    confirm = (
        input(f"Are you sure you want to uninstall {pkg}? (y/n): ").strip().lower()
    )
    if confirm == "y":
        output = run_adb(f"uninstall {pkg}")
        print(output)
    else:
        print("Uninstall canceled.")


def check_foreground_app(duration=10, interval=2):
    """Monitor foreground app in real-time for a set duration."""
    print(f"\nMonitoring foreground app for {duration} seconds...")
    for _ in range(duration // interval):
        output = run_adb("shell dumpsys window windows | grep mCurrentFocus")
        print(output)
        time.sleep(interval)


def list_overlay_permissions():
    """List apps allowed to draw over others."""
    output = run_adb("shell appops query-op SYSTEM_ALERT_WINDOW --user 0")
    print("\nApps allowed to display over others:")
    print(output)


def list_notification_permissions():
    """List apps allowed to post notifications."""
    output = run_adb("shell appops query-op POST_NOTIFICATION --user 0")
    print("\nApps allowed to post notifications:")
    print(output)


def main():
    while True:
        print("\n=== Interactive ADB Menu ===")
        print("1. List user-installed apps")
        print("2. Uninstall an app")
        print("3. Monitor foreground app")
        print("4. List apps with overlay permission")
        print("5. List apps allowed to post notifications")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            list_user_apps()
        elif choice == "2":
            uninstall_app()
        elif choice == "3":
            try:
                duration = int(
                    input("Duration to monitor (seconds, default 10): ") or "10"
                )
                interval = int(
                    input("Interval between checks (seconds, default 2): ") or "2"
                )
            except ValueError:
                duration, interval = 10, 2
            check_foreground_app(duration, interval)
        elif choice == "4":
            list_overlay_permissions()
        elif choice == "5":
            list_notification_permissions()
        elif choice == "6":
            print("Exiting…")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    print("Ensure your device has USB debugging enabled and is connected via ADB.")
    main()
