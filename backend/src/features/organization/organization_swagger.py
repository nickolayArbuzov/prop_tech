getManyByBuildingDoc = {
    200: {
        "description": "Successful response",
        "content": {
            "application/json": {
                "example": {
                    "data": [{"name": "string", "id": 0}],
                    "total": 0,
                    "page": 0,
                    "limit": 0,
                }
            }
        },
    }
}

getManyByActivityDoc = {
    200: {
        "description": "Successful response",
        "content": {
            "application/json": {
                "example": {
                    "data": [{"name": "string", "id": 0}],
                    "total": 0,
                    "page": 0,
                    "limit": 0,
                }
            }
        },
    }
}

getManyByGeoDoc = {
    200: {
        "description": "Successful response",
        "content": {
            "application/json": {
                "example": {
                    "data": [{"name": "string", "id": 0}],
                    "total": 0,
                }
            }
        },
    }
}

getOneByIdDoc = {
    200: {
        "description": "Successful response",
        "content": {
            "application/json": {
                "example": {
                    "name": "string",
                    "telephones": [{"phone_number": "string", "id": 0}],
                    "activities": [{"name": "string", "id": 0}],
                    "build": {
                        "address": "string",
                        "latitude": 55.752023,
                        "longitude": 37.586397,
                    },
                    "id": 0,
                }
            }
        },
    }
}

getManyByActivityAllDoc = {
    200: {
        "description": "Successful response",
        "content": {
            "application/json": {
                "example": {
                    "data": [{"name": "string", "id": 0}],
                    "total": 0,
                    "page": 0,
                    "limit": 0,
                }
            }
        },
    }
}

getByNameDoc = {
    200: {
        "description": "Successful response",
        "content": {
            "application/json": {
                "example": {
                    "data": [{"name": "string", "id": 0}],
                    "total": 0,
                    "page": 0,
                    "limit": 0,
                }
            }
        },
    }
}
