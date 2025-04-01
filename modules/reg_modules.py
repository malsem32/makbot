import modules.countries as countries
import modules.games as games
import modules.bonus as bonus
import modules.others.gpt as gpt
import modules.others.weather as weather
import modules.others.proxy as proxy

def reg_routers(dp):
    dp.include_routers(countries.router, games.router, bonus.router, gpt.router, weather.router, proxy.router)