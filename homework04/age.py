
from statistics import median
from typing import Optional
from datetime import datetime, date
from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    friends = get_friends(user_id, 'bdate')
    ages = []

    for friend in friends:
        user = User(**friend)
        if user.bdate and len(user.bdate) > 8:
            time_n = datetime.now()
            time_b = datetime.strptime(user.bdate, "%d.%m.%Y")
            u_age = (time_n - time_b)
            ages.append(int(u_age.days//365.25))

    return median(ages) if ages else None


print(age_predict(82770248))
