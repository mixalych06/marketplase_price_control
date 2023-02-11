
from create_bot import bot, dp, db
from handlers import users, admin


from aiogram.utils import executor
from pars_wildberris import all_pars, parsing_evry_day

import asyncio
from time import sleep


admin.register_handlers_admin(dp)
users.register_handlers_client(dp)

async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        users_list = db.select_users()
        for user in users_list:
            user_prod = db.all_product_in_user(user[0])
            if user_prod:
                for prod in user_prod:
                    try:
                        if prod[8]:
                            new_pars_produkt = parsing_evry_day(prod[7])
                        else:
                            new_pars_produkt = parsing_evry_day(prod[7])
                            await bot.send_message(user[0], text=f'<i><b>{prod[2]}</b></i>\nСнова в продаже')
                            db.changes_product_valye(prod[0], prod[1], 1)

                    except IndexError:
                        if prod[8]:
                            await bot.send_message(user[0], text=f'<i><b>{prod[2]}</b></i>\nСсылка удалена')
                            db.changes_product_valye(prod[0], prod[1], 0)

                    try:
                        if prod[8]:
                            if new_pars_produkt['salePriceU'] < prod[3] and new_pars_produkt['salePriceU'] < prod[4]:
                                '''шлём сообщение о снижении ценыб перезаписываем минималку и текущую'''
                                await bot.send_message(user[0], text=f'<i><b>{prod[2]}</b></i>\n<b>💸Цена снижена.💸</b>\nМеньше начальной цены на '
                                                                     f'{int(100 - ((new_pars_produkt["salePriceU"]//100) * 100 / (int(prod[3])//100)))}%\n'
                                                                     f'Цена минимальная🤑 с момента отслеживания.\n'
                                                                     f'<i>{prod[7]}</i>', parse_mode='HTML')
                                db.changes_product_data((new_pars_produkt['salePriceU'], new_pars_produkt['salePriceU'], prod[0], prod[1]))

                                continue
                            elif new_pars_produkt['salePriceU'] < prod[5] and new_pars_produkt['salePriceU'] >= prod[4] and new_pars_produkt['salePriceU'] < prod[3]:
                                '''сообщение о снижении, перезаписываем текущую'''
                                await bot.send_message(user[0], text=f'<i><b>{prod[2]}</b></i>\n<b>💸Цена снижена.💸</b>\nМеньше начальной цены на'
                                                                     f'{int(100 - ((new_pars_produkt["salePriceU"] // 100) * 100 / (int(prod[3]) // 100)))}%\n'
                                                                     f'<i>{prod[7]}</i>', parse_mode='HTML')
                                db.changes_product_data((prod[4], new_pars_produkt['salePriceU'], prod[0], prod[1]))

                                continue
                            else:
                                db.changes_product_data((prod[4], new_pars_produkt['salePriceU'], prod[0], prod[1]))

                    except:

                        db.off_user(prod[0])
            else:

                continue

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(10800))
    executor.start_polling(dp, skip_updates=True)
