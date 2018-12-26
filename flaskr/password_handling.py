from werkzeug.security import check_password_hash, generate_password_hash



def HashPassword(password):
  hash = generate_password_hash(password)
  return hash
  
def IsPasswordHashesEqual(password_A, password_B):
  result = check_password_hash(password_A, password_B)
  if result:
    return True
  return False