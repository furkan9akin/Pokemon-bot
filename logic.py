import aiohttp
import random
from random import randint

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.img = None
        self.power = random.randint(30, 60)
        self.hp = random.randint(200, 400)
        if pokemon_trainer not in self.pokemons:
            self.pokemons[pokemon_trainer] = self

    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                else:
                    return "Pikachu"

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        return f"""Nama Pokémon Anda: {self.name}
                : {self.power}
                Здоровье покемона: {self.hp}"""

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    img_url = data['sprites']['front_default']
                    return img_url 
                else:
                    return None

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance == 1:
                return "Pokémon Wizard menggunakan pelindung saat pertarungan!"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pemilik Pokémon @{self.pokemon_trainer} menyerang @{enemy.pokemon_trainer}\nKesehatan @{enemy.pokemon_trainer} sekarang adalah {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pemilik Pokémon @{self.pokemon_trainer} mengalahkan @{enemy.pokemon_trainer}!"

class Wizard(Pokemon):
    # Metode dan properti khusus untuk kelas Wizard
    pass

class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = randint(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nPokémon Fighter menggunakan serangan super. Tambahkan daya sebesar: {super_power}"

class Wizard(Pokemon):
    # Pada kelas ini, kita dapat menambahkan metode dan properti khusus untuk kelas Wizard
    pass

class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = randint(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nPokémon Fighter menggunakan serangan super. Tambahkan daya sebesar: {super_power}"
    

"""if __name__ == "__main__":
    pikachu = Pokemon("alex")
    bounsweet = Pokemon("steve")
    pikachu.hp = 35
    pikachu.attack = 55
    bounsweet.hp = 42
    bounsweet.attack = 30
    pikachu.info()
    bounsweet.info()
    print("*"* 50)
    pikachu.aattack(bounsweet)"""
