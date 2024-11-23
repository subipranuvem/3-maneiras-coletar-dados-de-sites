from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import json


driver = webdriver.Chrome()
driver.get("https://pokemondb.net/pokedex/all")

table_lines = driver.find_elements(By.CSS_SELECTOR, "table.data-table tbody tr")
data = []
for table_line in table_lines:
    columns = table_line.find_elements(By.TAG_NAME, "td")
    pokemon_name = columns[1].text.replace("\n", "-")
    pokemon_types = [
        t.text for t in columns[2].find_elements(By.CLASS_NAME, "type-icon")
    ]
    pokemon_img_url = columns[0].find_element(By.TAG_NAME, "img").get_attribute("src")
    data.append(
        [
            columns[0].text,  # Number
            pokemon_name,
            json.dumps(pokemon_types),
            pokemon_img_url,
            *[col.text for col in columns[3:8]],  # Total, HP, Attack, Defense, Speed
        ]
    )
    print(f"collected data from pokemon [{columns[0].text}] -> {pokemon_name}")

driver.quit()

with open("detailed_pokemon.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "pokedex_number",
            "name",
            "types",
            "image_url",
            "total",
            "hp",
            "attack",
            "defense",
            "speed",
        ]
    )
    writer.writerows(data)
