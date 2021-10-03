from django.urls import path

from card.views import AddCardView, GetAllCardsView, DeleteCardView, RefundCard

urlpatterns = [
    path('card/add/', AddCardView.as_view()),
    path('card/list/', GetAllCardsView.as_view()),
    path('card/delete/', DeleteCardView.as_view()),
    path('card/refund/', RefundCard.as_view()),
]
