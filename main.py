# main.py
import argparse
from workspace.config.task_registry import get_task
from workspace.tools.logger.stdout_tee import enable_stdout_logging
from workspace.config import paths


def main():
    # ✅ 啟用 stdout Tee，把所有 print 同步寫到 log 檔與主控台
    log_file = paths.generate_log_path()
    enable_stdout_logging(log_file, overwrite=True, also_stderr=True)
    print(f"[INFO] Logging enabled, file={log_file}")

    parser = argparse.ArgumentParser(
        description="入口檔：選擇任務 / 控制器 / 工具來執行"
    )
    parser.add_argument(
        "category", choices=["task", "controller", "tool"], help="任務類型"
    )
    parser.add_argument("id", help="任務/控制器/工具 ID")
    parser.add_argument("--debug", action="store_true", help="開啟除錯模式")

    args = parser.parse_args()

    task_func = get_task(args.category, args.id)

    if not task_func:
        print(f"[❌] 找不到 {args.category}:{args.id}")
        return

    if args.debug:
        print(f"[DEBUG] 執行 {args.category}:{args.id}")

    task_func()


if __name__ == "__main__":
    main()
