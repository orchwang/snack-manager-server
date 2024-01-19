from typing import Optional

from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

from snack.core.serializers.general_serializers import ResponseDetailSerializer
from snack.order.constants import SnackReactionType
from snack.order.serializers.snack_serializers import (
    SnackSerializer,
    SnackReactionWriteSerializer,
    SnackWriteSerializer,
)
from snack.order.models import Snack, SnackReaction
from snack.order.exceptions import InvalidSnack, InvalidSnackReaction

User = get_user_model()


@extend_schema(description='등록된 간식 목록을 불러옵니다.', responses={200: SnackSerializer}, methods=['GET'])
@extend_schema(
    description='새로운 간식을 등록합니다.',
    request=SnackWriteSerializer,
    responses={201: SnackSerializer},
    methods=['POST'],
)
class SnackView(generics.ListCreateAPIView):
    queryset = Snack.objects.prefetch_related('snack_reactions')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SnackWriteSerializer
        return SnackSerializer


@extend_schema(
    description='특정 간식의 리액션을 토글 합니다.',
    request={'type': SnackReactionType},
    responses={200: ResponseDetailSerializer},
    methods=['POST'],
)
class SnackReactionViewSet(viewsets.ViewSet):
    """
    TODO: Viewset 경험을 위해 구성한 View 이다.
          해당 API 의 용도에 맞게 사용했다는 생각은 들이 않는다.
          또한 endpoint 인 `/order/<str:uid>/reactions/` 은
          Resource 중심의 RESTful 에 어울리지 않는다는 생각이다.
          아이디어가 필요하다.
    """

    def create(self, request, **kwargs) -> Response:
        snack_uid = kwargs['uid']
        reaction_type_payload = request.data.get('type')

        try:
            reaction_type = SnackReactionType(reaction_type_payload)
        except ValueError:
            raise InvalidSnackReaction(f'{reaction_type_payload} is invalid snack reaction.')

        snack = self._get_snack_obj(snack_uid)

        self._process_toggle_reaction(snack, request.user, reaction_type)

        return Response({'detail': 'success'}, status=status.HTTP_200_OK)

    def _get_snack_obj(self, snack_uid: str) -> Optional[Snack]:
        try:
            return Snack.objects.get(uid=snack_uid)
        except Snack.DoesNotExist:
            raise InvalidSnack(f'Snack not found with uid "{snack_uid}".')

    def _process_toggle_reaction(
        self, snack: Optional[Snack], user: Optional[User], reaction_type: Optional[SnackReactionType]
    ):
        try:
            # Check existing reaction
            snack_reaction = SnackReaction.objects.get(snack=snack, user=user)

            # Check duplicated reaction
            if snack_reaction.type == reaction_type:
                raise InvalidSnackReaction('You cannot react same reaction.')
            else:
                # Toggle if opposite reaction exists
                snack_reaction.delete()
                self._create_reaction(snack.uid, user.id, reaction_type)
        except SnackReaction.DoesNotExist:
            self._create_reaction(snack.uid, user.id, reaction_type)

    def _create_reaction(self, snack_uid: str, user_id: str, reaction_type: Optional[SnackReactionType]):
        serializer = SnackReactionWriteSerializer(
            data={
                'snack': snack_uid,
                'user': user_id,
                'type': reaction_type,
            }
        )
        serializer.is_valid()
        serializer.save()
