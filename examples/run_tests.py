from src.testing.test_framework import AmmeterTestFramework

def main():
    # יצירת מסגרת הבדיקות
    framework = AmmeterTestFramework("../config/config.yaml")
    framework.run_test(framework.config)

if __name__ == "__main__":
    main() 