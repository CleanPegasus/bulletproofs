from py_ecc.bn128 import G1, field_modulus, FQ, curve_order, is_on_curve, multiply, add, Z1
import hashlib
import sympy

def bytes_to_field_element(bytes_input):
    """Convert bytes to field element using little-endian interpretation"""
    return int.from_bytes(bytes_input, byteorder='little') % field_modulus

def generate_random_point(seed):
    """Generate a random point on the curve using the seed"""
    # First hash of seed to bytes
    hash_bytes = hashlib.sha256(seed.encode('utf-8')).digest()
    # Convert to field element using little-endian
    x = bytes_to_field_element(hash_bytes)
    # Get next hash for seed
    next_hash = hashlib.sha256(hash_bytes).digest().hex()
    
    # Find valid point
    while True:
        x_fq = FQ(x)
        y_squared = x_fq**3 + FQ(3)
        
        # Try to find y coordinate
        if y_squared ** ((field_modulus - 1) // 2) == FQ(1):
            y = sympy.sqrt_mod(int(y_squared), field_modulus)
            point = [FQ(x), FQ(y)]
            if is_on_curve(point, FQ(3)):
                return point, next_hash
        
        x = (x + 1) % field_modulus

def generate_n_random_points(seed, n):
    """Generate n random points starting from seed"""
    result = []
    current_seed = seed
    
    for _ in range(n):
        point, next_seed = generate_random_point(current_seed)
        result.append(point)
        current_seed = next_seed
    
    return result

# Test function
def test_point_generation():
    """Test function to verify points are on curve"""
    seed = "hello"
    points = generate_n_random_points(seed, 2)
    
    print("Generated points:")
    for i, point in enumerate(points):
        valid = is_on_curve(point, FQ(3))
        print(f"Point {i+1}:")
        print(f"x: {point[0]}")
        print(f"y: {point[1]}")
        print(f"Is on curve: {valid}\n")

test_point_generation()