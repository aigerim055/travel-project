from rest_framework import serializers

from .models import (
    TourPurchase, 
    TourItems
)
from .utils import cashback


class TourItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourItems
        fields = ['tour', 'people_num']


class TourPurchaseSerializer(serializers.ModelSerializer):
    items = TourItemsSerializer(many=True) 

    class Meta:
        model = TourPurchase
        fields = ['order_id', 'created_at', 'total_sum', 'items']

    def create(self, validated_data, *args, **kwargs):
        items = validated_data.pop('items')
        validated_data['user'] = self.context['request'].user
        order = super().create(validated_data) # Order.objects.create
        total_sum = 0
        orders_items = []
        for item in items:
            tickets = (TourItems(
                order=order,
                tour=item['tour'],
                people_num=item['people_num']
            ))
            orders_items.append(tickets)

            if item['tour'].people_count >= item['people_num']:
                item['tour'].people_count -= item['people_num']

                total_sum += item['tour'].price_som * item['people_num']
                TourItems.objects.bulk_create(orders_items, *args, **kwargs)
                order.total_sum = total_sum

                order.create_code()
                
                if self.context['request'].user.is_authenticated:
                    cashback(self.context, order, total_sum, item['tour'].tour.company_name)

                item['tour'].save()
                order.save()

                return order
            else:
                raise serializers.ValidationError('Недостаточно свободных мест.')


class PurchaseHistorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TourPurchase
        fields = ('order_id', 'total_sum', 'status', 'created_at', 'tour')