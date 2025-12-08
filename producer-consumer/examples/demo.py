import sys
sys.path.insert(0, '..')

from main import ProducerConsumerPipeline
import time
from datetime import datetime


def create_work_items(count):
    """Create simple work items for demo"""
    items = []
    for i in range(1, count + 1):
        items.append({
            'id': i,
            'data': f'Item-{i:03d}'
        })
    return items


def print_header(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_separator():
    """Print separator"""
    print("-" * 70)


def visualize_buffer(size, capacity):
    """Create visual buffer representation"""
    filled = '#' * size
    empty = '.' * (capacity - size)
    bar = f"[{filled}{empty}]"

    # Show blocking states
    if size == capacity:
        state = "FULL (Producer blocked)"
    elif size == 0:
        state = "EMPTY (Consumer waiting)"
    else:
        state = "Available"

    return f"{bar} {size}/{capacity} {state}"


def on_produce(item, count, buffer_size):
    """Callback when item is produced"""
    ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    buffer_visual = visualize_buffer(buffer_size, 5)
    print(f"[{ts}] PRODUCE -> {item['data']}  |  Buffer: {buffer_visual}")


def on_consume(item, count, buffer_size):
    """Callback when item is consumed"""
    ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    buffer_visual = visualize_buffer(buffer_size, 5)
    print(f"[{ts}] CONSUME <- {item['data']}  |  Buffer: {buffer_visual}")


def print_summary(stats, start_time, end_time):
    """Print execution summary"""
    duration = end_time - start_time

    print_separator()
    print_header("Execution Summary")
    print(f"  Items Produced:  {stats['produced']}")
    print(f"  Items Consumed:  {stats['consumed']}")
    print(f"  Duration:        {duration:.2f}s")
    print(f"  Verification:    {'PASS - All items processed' if stats['success'] else 'FAIL'}")
    print_separator()


def run_mode_1():
    """Balanced: Producer and consumer run at same speed"""
    print_header("Mode 1: Balanced Throughput")
    print("  Producer: produces every 0.3s")
    print("  Consumer: consumes every 0.3s")
    print("  Buffer:   capacity = 5")
    print("\n  Expected behavior:")
    print("    - Smooth flow, minimal blocking")
    print("    - Buffer stays partially filled")
    print_separator()

    time.sleep(1)

    pipeline = ProducerConsumerPipeline(buffer_capacity=5)
    items = create_work_items(12)

    start = time.time()
    pipeline.process(
        items,
        producer_delay=0.3,
        consumer_delay=0.3,
        on_produce=on_produce,
        on_consume=on_consume
    )
    end = time.time()

    print_summary(pipeline.get_stats(), start, end)


def run_mode_2():
    """Backpressure: Fast producer, slow consumer"""
    print_header("Mode 2: Backpressure (Fast Producer)")
    print("  Producer: produces every 0.2s")
    print("  Consumer: consumes every 0.6s")
    print("  Buffer:   capacity = 5")
    print("\n  Expected behavior:")
    print("    - Buffer fills to capacity")
    print("    - Producer BLOCKS when buffer full")
    print("    - Demonstrates thread synchronization")
    print_separator()

    time.sleep(1)

    pipeline = ProducerConsumerPipeline(buffer_capacity=5)
    items = create_work_items(12)

    print("\nWatch for 'FULL (Producer blocked)' state:\n")
    time.sleep(0.5)

    start = time.time()
    pipeline.process(
        items,
        producer_delay=0.2,
        consumer_delay=0.6,
        on_produce=on_produce,
        on_consume=on_consume
    )
    end = time.time()

    print_summary(pipeline.get_stats(), start, end)


def run_mode_3():
    """Starvation: Slow producer, fast consumer"""
    print_header("Mode 3: Starvation (Slow Producer)")
    print("  Producer: produces every 0.6s")
    print("  Consumer: consumes every 0.2s")
    print("  Buffer:   capacity = 5")
    print("\n  Expected behavior:")
    print("    - Buffer stays mostly empty")
    print("    - Consumer WAITS when buffer empty")
    print("    - Demonstrates consumer blocking")
    print_separator()

    time.sleep(1)

    pipeline = ProducerConsumerPipeline(buffer_capacity=5)
    items = create_work_items(12)

    print("\nWatch for 'EMPTY (Consumer waiting)' state:\n")
    time.sleep(0.5)

    start = time.time()
    pipeline.process(
        items,
        producer_delay=0.6,
        consumer_delay=0.2,
        on_produce=on_produce,
        on_consume=on_consume
    )
    end = time.time()

    print_summary(pipeline.get_stats(), start, end)


def run_mode_4():
    """Small buffer: Shows blocking with minimal capacity"""
    print_header("Mode 4: Small Buffer (Capacity = 2)")
    print("  Producer: produces every 0.3s")
    print("  Consumer: consumes every 0.4s")
    print("  Buffer:   capacity = 2 (reduced)")
    print("\n  Expected behavior:")
    print("    - Frequent blocking due to small buffer")
    print("    - Producer blocks often")
    print("    - Shows impact of buffer size on throughput")
    print_separator()

    time.sleep(1)

    pipeline = ProducerConsumerPipeline(buffer_capacity=2)
    items = create_work_items(10)

    print("\nSmall buffer means more blocking:\n")
    time.sleep(0.5)

    start = time.time()
    pipeline.process(
        items,
        producer_delay=0.3,
        consumer_delay=0.4,
        on_produce=on_produce,
        on_consume=on_consume
    )
    end = time.time()

    print_summary(pipeline.get_stats(), start, end)


def show_welcome():
    """Display welcome screen"""
    print("\n")
    print("+" + "=" * 68 + "+")
    print("|" + " " * 68 + "|")
    print("|" + "  Producer-Consumer Pattern - Thread Synchronization Demo".ljust(69) + "|")
    print("|" + " " * 68 + "|")
    print("+" + "=" * 68 + "+")
    print("\n  Demonstrates:")
    print("    - Concurrent thread execution")
    print("    - Bounded buffer (blocking queue)")
    print("    - Thread synchronization with Condition variables")
    print("    - Backpressure handling")
    print("\n  Key Concepts:")
    print("    - When buffer FULL  -> Producer blocks (waits)")
    print("    - When buffer EMPTY -> Consumer blocks (waits)")
    print("    - Condition.wait() and Condition.notify() coordinate threads")
    print("\n")
    print_separator()
    print("Available Modes:")
    print_separator()
    print("\n  1. Balanced       - Equal speeds, smooth flow")
    print("  2. Backpressure   - Fast producer, buffer fills, blocking demo")
    print("  3. Starvation     - Slow producer, buffer empties, waiting demo")
    print("  4. Small Buffer   - Buffer size = 2, frequent blocking")
    print("  5. Exit")
    print("\n")
    print_separator()


def main():
    """Main interactive loop"""
    while True:
        show_welcome()

        try:
            choice = input("\n> Select mode (1-5): ").strip()

            if choice == '1':
                run_mode_1()
            elif choice == '2':
                run_mode_2()
            elif choice == '3':
                run_mode_3()
            elif choice == '4':
                run_mode_4()
            elif choice == '5':
                print("\nExiting.\n")
                break
            else:
                print("\n[ERROR] Invalid choice. Select 1-5.")
                time.sleep(1)
                continue

            print("\n")
            again = input("Run another mode? (y/n): ").strip().lower()
            if again != 'y':
                print("\nExiting.\n")
                break

        except KeyboardInterrupt:
            print("\n\nInterrupted.\n")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()