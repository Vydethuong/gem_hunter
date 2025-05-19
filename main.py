import time
from utils import read_input_file, write_output_file, print_grid
from solver_pysat import solve_with_pysat, gen_cnf_from_grid
from bruteforce import brute_force_parallel
from backtracking import solve_backtracking

def main():
    print("Chọn phương pháp giải:")
    print("1. PySAT")
    print("2. Brute-force")
    print("3. Backtracking")

    method = input("Nhập lựa chọn (1/2/3): ").strip()
    input_file = input("Nhập tên file input (ví dụ: testcases/input1.txt): ").strip()
    output_file = input("Nhập tên file output (ví dụ: testcases/output1.txt): ").strip()

    grid = read_input_file(input_file)

    cnf = gen_cnf_from_grid(grid)

    start_time = time.time()

    if method == '1':
        print("\n[+] Đang giải bằng PySAT...")
        result = solve_with_pysat(grid,cnf)
    elif method == '2':
        print("\n[+] Đang giải bằng Brute-force...")
        result = brute_force_parallel(grid, cnf, timeout=300) 
    elif method == '3':
        print("\n[+] Đang giải bằng Backtracking...")
        result = solve_backtracking(grid, cnf)  
    else:
        print("Lựa chọn không hợp lệ.")
        return

    elapsed_time = time.time() - start_time

    if result:
        print("\nTìm được lời giải! Kết quả:")
        print_grid(result)
        write_output_file(result, output_file)
        print(f"\nĐã ghi kết quả vào: {output_file}")
    else:
        print("Không tìm được lời giải.")

    print(f"Thời gian chạy: {elapsed_time:.4f} giây")

if __name__ == '__main__':
    main()
