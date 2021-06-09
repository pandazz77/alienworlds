*New captcha solver: anticaptcha
*Removed unnecessary functions (only for farm mode)
*exec_stop in working
*New config
------------------------------------
Конфиг настраивается в формате json
farm_cords - Массив с парами координат вашего браузера в виде [[x,y],[x1,y1]]
oth_mons - Целое число суммы пикселей по оси X мониторов, установленных слева от основного монитора (Если у вас 1 монитор - выставляйте значение 0)
calibrate - Настройка калибровочного пикселя (Не меняйте значение)
eoe - "Exit on Error", true - выключить бота после ошибки, false - продолжить работу
farm_attemp_limit - Количество тиков, при котором бот, не обнаружив ни одной кнопки перейдет к следующему профилю
claiming_timer_limit - Лимит claiming TLM'а, при котором бот перезагрузит страницу
mining_timer_limit - Лимит Mining Progress'a, при котором бот перезагрузит страницу