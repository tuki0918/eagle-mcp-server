from pydantic import BaseModel, Field
from typing import Annotated, Dict, Optional, List, Literal, Union
from schemas import SuccessResponse, ErrorResponse


class AddBaseItem(BaseModel):
    name: Annotated[
        str, Field(..., description="Required, the name of the image to be added.")
    ]
    # APIのドキュメントによっては、項目名がurlの場合がある
    website: Annotated[
        Optional[str], Field(None, description="The Address of the source of the image")
    ]
    tags: Annotated[Optional[List[str]], Field(None, description="Tags for the image.")]
    # APIのドキュメントによっては、記載されていない場合がある。実際には利用可能
    star: Annotated[
        Optional[int], Field(None, ge=0, le=5, description="The rating for the image.")
    ]
    annotation: Annotated[
        Optional[str], Field(None, description="The annotation for the image.")
    ]


class AddBaseItemFromURL(AddBaseItem):
    url: Annotated[
        str,
        Field(
            ...,
            description="Required, the URL of the image to be added. Supports http, https, base64",
        ),
    ]
    modificationTime: Annotated[
        Optional[int],
        Field(
            None,
            description="The creation date (ms) of the image. The parameter can be used to alter the image's sorting order in Eagle.",
        ),
    ]
    headers: Annotated[
        Optional[Dict[str, str]],
        Field(
            None,
            description="Optional, customize the HTTP headers properties, this could be used to circumvent the security of certain websites.",
        ),
    ]


class AddBaseItemFromPath(AddBaseItem):
    path: Annotated[
        str, Field(..., description="Required, the path of the local file.")
    ]


class AddItemFromURLRequest(AddBaseItemFromURL):
    folderId: Annotated[
        Optional[str],
        Field(
            None,
            description="If this parameter is defined, the image will be added to the corresponding folder.",
        ),
    ]


class AddItemsFromURLsRequest(BaseModel):
    items: Annotated[
        List[AddBaseItemFromURL],
        Field(
            ...,
            description="The array object made up of multiple items (See the description below)",
        ),
    ]
    folderId: Annotated[
        Optional[str],
        Field(
            None,
            description="If the parameter is defined, images will be added to the corresponding folder.",
        ),
    ]


class AddItemFromPathRequest(AddBaseItemFromPath):
    folderId: Annotated[
        Optional[str],
        Field(
            None,
            description="If this parameter is defined, the image will be added to the corresponding folder.",
        ),
    ]


class AddItemsFromPathsRequest(BaseModel):
    # ドキュメントがおそらく間違っている。
    items: Annotated[
        List[AddBaseItemFromPath],
        Field(
            ...,
            description="The array object made up of multiple items (See the description below)",
        ),
    ]
    folderId: Annotated[
        Optional[str],
        Field(
            None,
            description="If this parameter is defined, the image will be added to the corresponding folder.",
        ),
    ]


class GetItemInfoRequest(BaseModel):
    id: Annotated[
        str,
        Field(
            ...,
            description="ID of the file",
        ),
    ]


class GetItemThumbnailRequest(BaseModel):
    id: Annotated[
        str,
        Field(
            ...,
            description="ID of the file",
        ),
    ]


class GetItemListRequest(BaseModel):
    limit: Annotated[
        Optional[int],
        Field(
            200,
            ge=1,
            le=200,
            description="The number of items to be displayed. the default number is `200`",
        ),
    ]
    offset: Annotated[
        Optional[int],
        Field(
            0,
            ge=0,
            description="Offset a collection of results from the api. Start with `0`",
        ),
    ]
    orderBy: Annotated[
        Optional[str],
        Field(
            None,
            description="The sorting order. `CREATEDATE`, `FILESIZE`, `NAME`, `RESOLUTION`, add a minus sign for descending order: `-FILESIZE`",
        ),
    ]
    keyword: Annotated[Optional[str], Field(None, description="Filter by the keyword")]
    ext: Annotated[
        Optional[str],
        Field(None, description="Filter by the extension type, e.g.: `jpg`, `png`"),
    ]
    tags: Annotated[
        Optional[str],
        Field(
            None,
            description="Filter by tags. Use `,` to divide different tags. E.g.: `Design, Poster`",
        ),
    ]
    folders: Annotated[
        Optional[str],
        Field(
            None,
            description="Filter by Folders. Use `,` to divide folder IDs. E.g.: `KAY6NTU6UYI5Q,KBJ8Z60O88VMG`",
        ),
    ]


class UpdateItemRequest(BaseModel):
    id: Annotated[
        str,
        Field(
            ...,
            description="Required, the ID of the item to be modified",
        ),
    ]
    tags: Annotated[Optional[List[str]], Field(None, description="Optional, tags")]
    annotation: Annotated[
        Optional[str], Field(None, description="Optional, annotations")
    ]
    url: Annotated[Optional[str], Field(None, description="Optional, the source url")]
    star: Annotated[
        Optional[int], Field(None, ge=0, le=5, description="Optional, ratings")
    ]


class GetItemSourceRequest(BaseModel):
    id: Annotated[
        str,
        Field(
            ...,
            description="ID of the file",
        ),
    ]


class GetItemSourceSuccessResponse(SuccessResponse):
    data: Annotated[
        Dict[Literal["source"], str],
        Field(...),
    ]


GetItemSourceResponse = Union[GetItemSourceSuccessResponse, ErrorResponse]
