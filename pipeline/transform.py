import pandas as pd

def clean_data(productos):
    df = pd.DataFrame(productos)

    df = df[
        (df['price'] != "No disponible") &
        (df['product_name'].notna()) & (df['product_name'] != "No disponible") & (df['product_name'].str.strip() != "") &
        (df['brand'].notna()) & (df['brand'] != "No disponible") & (df['brand'].str.strip() != "")
    ]

    # Limpiar columna de precio
    df['price'] = df['price'].astype(str)
    df['price'] = df['price'].str.replace(r'[$.]', '', regex=True).str.strip()
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna(subset=['price'])
    df['price'] = df['price'].astype(int)

    # Formatear texto: primera letra en mayúscula, resto en minúscula
    columnas_texto = ['product_name', 'brand', 'category', 'market_name']
    for col in columnas_texto:
        df[col] = df[col].astype(str).str.strip().str.capitalize()

    return df
