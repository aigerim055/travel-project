from apps.bio.models import UserProfile
from .tasks import send_details


def cashback(context, order, total_sum, company):
    user = context['request'].user
    profile = UserProfile.objects.get(user=user)
    company = str(company)

    if profile:
        cashback = profile.cashback
        print('cash', cashback)
        if not cashback:
            reward = 0
            order.total_sum = total_sum
            collected_sum = total_sum
            cashback.append({company: {"cashback": 0, "collected_sum": collected_sum}})
            profile.save()
        else:
            for comp in cashback:
                if company in comp.keys():
                    reward = int(comp[company]['cashback'])
                    order.total_sum = total_sum - total_sum*reward/100
                    collected_summ = comp[company]['collected_sum']
                    comp[company]['collected_sum'] += order.total_sum
                    collected_summ += order.total_sum

                    if collected_summ >= 10000:
                        comp[company]['cashback'] = 3

                    if collected_summ >= 20000:
                        comp[company]['cashback'] = 5

                    if collected_summ >= 50000:
                        comp[company]['cashback'] = 7

                    if collected_summ >= 100000:
                        comp[company]['cashback'] = 10
                profile.save()

        order.save()
        email = user.email
        code = order.code
        send_details(email, code)
        # send_details.delay(email, code)
    
    elif not profile:
        return 'Чтобы получить скидку, заполните свой профиль.'