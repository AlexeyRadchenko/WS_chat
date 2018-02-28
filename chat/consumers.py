from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ClientError(Exception):

    def __init__(self, code):
        super().__init__(code)
        self.code = code


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.accept()

    async def receive_json(self, content, **kwargs):
        command = content.get('command', None)
        try:
            if command == 'join':
                await self.channel_layer.group_add(
                    'MainChannelGroup',
                    self.channel_name,
                )
                await self.send_json({
                    "join": '1',
                    "title": 'MainRoom1',
                })
                await self.channel_layer.group_send(
                    'MainChannelGroup',
                    {
                        "type": "chat.join",
                        "room": '1',
                        "username": self.scope["user"].username,
                    }
                )

            elif command == 'send':
                await self.channel_layer.group_send(
                    'MainChannelGroup',
                    message={
                        "type": "chat.message",
                        "room": '1',
                        "username": self.scope["user"].username,
                        "message": content.get('message', None),
                    }
                )

        except ClientError as e:
            self.send_json({"error": e.code})

    async def chat_join(self, event):

        await self.send_json(
            {
                "msg_type": 1,
                "room": event["room"],
                "username": event["username"],
            },
        )

    async def chat_message(self, event):
        await self.send_json(
            {
                "msg_type": 0,
                "room": event["room"],
                "username": event["username"],
                "message": event["message"],
            },
        )


