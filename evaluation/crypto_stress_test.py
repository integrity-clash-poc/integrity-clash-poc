import json
import time
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

# --- Benchmark Configuration ---
ITERATIONS = 10000
TIME_BUDGET_SEC = 2.0
PAYLOAD = json.dumps({"status": "COMPLETED", "task_id": "TASK_001"}).encode('utf-8')

def run_stress_test():
    # 1. Benchmark Key Generation
    start_time = time.perf_counter()
    keys = [ec.generate_private_key(ec.SECP256R1()) for _ in range(ITERATIONS)]
    keygen_time = (time.perf_counter() - start_time) / ITERATIONS

    # Extract single keypair for isolated sign/verify testing
    private_key = keys[0]
    public_key = private_key.public_key()

    # 2. Benchmark Signature Generation
    start_time = time.perf_counter()
    signatures = [private_key.sign(PAYLOAD, ec.ECDSA(hashes.SHA256())) for _ in range(ITERATIONS)]
    sign_time = (time.perf_counter() - start_time) / ITERATIONS
    
    signature = signatures[0]

    # 3. Benchmark Signature Verification
    start_time = time.perf_counter()
    for _ in range(ITERATIONS):
        public_key.verify(signature, PAYLOAD, ec.ECDSA(hashes.SHA256()))
    verify_time = (time.perf_counter() - start_time) / ITERATIONS

    # --- Calculations ---
    combined_time = sign_time + verify_time
    
    def to_ms(t): return t * 1000
    def max_ops(t): return int(TIME_BUDGET_SEC / t)

    # --- Output formatting ---
    print(f"| Operation | Time per Operation (ms) | Max Operations in 2.0s window |")
    print(f"| :--- | :--- | :--- |")
    print(f"| Key Generation | {to_ms(keygen_time):.4f} | {max_ops(keygen_time):,} |")
    print(f"| Signature Generation | {to_ms(sign_time):.4f} | {max_ops(sign_time):,} |")
    print(f"| Signature Verification | {to_ms(verify_time):.4f} | {max_ops(verify_time):,} |")
    print(f"| Combined (Sign + Verify) | {to_ms(combined_time):.4f} | {max_ops(combined_time):,} |")

if __name__ == "__main__":
    run_stress_test()