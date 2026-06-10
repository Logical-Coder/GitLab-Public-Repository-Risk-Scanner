from rest_framework import serializers



class ScanSerializer(serializers.Serializer):

    target_type = serializers.ChoiceField(
        choices=[
            "user",
            "group",
            "repository"
        ]
    )

    target_name = serializers.CharField()