from sympy import factorint

N = 510143758735509025530880200653196460532653147

factors = factorint(N, use_ecm=True)  # ECM se usa automáticamente para números grandes
print(factors)


# se obtuvo :{19704762736204164635843: 1, 25889363174021185185929: 1}
a = 19704762736204164635843
b = 25889363174021185185929

print(min(a, b))
# resultado 19704762736204164635843
