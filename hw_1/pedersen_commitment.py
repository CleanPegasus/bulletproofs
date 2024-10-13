# %%
from py_ecc.bn128 import G1, field_modulus, FQ, curve_order, is_on_curve, multiply, add, Z1
import hashlib
import sympy

# %%
def generate_random_point(seed):
    hash_object = hashlib.sha256()
    hash_object.update(seed.encode('utf-8'))
    seed_hash_hex = hash_object.hexdigest()
    seed_hash = int(seed_hash_hex, 16)
    
    return seed_hash % field_modulus

# %%

def is_x_on_curve(x):
    x = FQ(x)
    y_squared = x**3 + FQ(3)
    return has_square_root(y_squared)

def has_square_root(n):
    # Euler's criterion
    return n**((field_modulus - 1) // 2) == FQ(1)

# %%
def find_y(x):
    x = FQ(x)
    y_squared = x**3 + FQ(3)
    if not is_x_on_curve(x):
        return None
    y = sympy.sqrt_mod(int(y_squared), field_modulus)
    return y

# %%
def generate_valid_point(seed):
  x = generate_random_point(seed)
  while not is_x_on_curve(x):
    x = x + 1 % field_modulus
  y = find_y(x)
  return [FQ(x), FQ(y)]

# %%
def generate_next_seed(seed):
    hash_object = hashlib.sha256()
    hash_object.update(seed.encode('utf-8'))
    seed_hash_hex = hash_object.hexdigest()
    return seed_hash_hex

# %%
def generate_n_random_points(seed, n):
  result = []
  for i in range(n):
    valid_point = generate_valid_point(seed)
    seed = generate_next_seed(seed)
    result.append(valid_point)

  return result
  

# %%
valid_points = generate_n_random_points("goblin-plonk", 10)

# %%
valid_points

# %%
def pedersen_commitment(vector, blinding_factor, seed):
  commitment = Z1
  vector_len = len(vector)
  random_points = generate_n_random_points(seed, vector_len + 1)
  
  for i in range(vector_len):
    commitment = add(commitment, multiply(random_points[i], vector[i]))
  
  commitment = add(commitment, multiply(random_points[vector_len - 1], blinding_factor))

  return commitment


# %%
commitment = pedersen_commitment([1, 2, 3, 4], 100, 'hello')

# %%
commitment

# %%



