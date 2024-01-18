from datetime import datetime
from typing import List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    HttpUrl,
    ValidationError,
    validator,
)


class TypesBaseModel(BaseModel):
    model_config = ConfigDict(
        coerce_numbers_to_str=True
    )  # (jarrodnorwell) fixed city_id issue


def validate_external_url(cls, v):
    if v is None or (v.startswith("http") and "://" in v) or isinstance(v, str):
        return v
    raise ValidationError("external_url must been URL or string")


class Resource(TypesBaseModel):
    pk: str
    video_url: Optional[HttpUrl] = None  # for Video and IGTV
    thumbnail_url: HttpUrl
    media_type: int


class User(TypesBaseModel):
    pk: str
    username: str
    full_name: str
    is_private: bool
    profile_pic_url: HttpUrl
    profile_pic_url_hd: Optional[HttpUrl] = None
    is_verified: bool
    media_count: int
    follower_count: int
    following_count: int
    biography: Optional[str] = ""
    external_url: Optional[str] = None
    account_type: Optional[int] = None
    is_business: bool

    public_email: Optional[str] = None
    contact_phone_number: Optional[str] = None
    public_phone_country_code: Optional[str] = None
    public_phone_number: Optional[str] = None
    business_contact_method: Optional[str] = None
    business_category_name: Optional[str] = None
    category_name: Optional[str] = None
    category: Optional[str] = None

    address_street: Optional[str] = None
    city_id: Optional[str] = None
    city_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    zip: Optional[str] = None
    instagram_location_id: Optional[str] = None
    interop_messaging_user_fbid: Optional[str] = None

    _external_url = validator("external_url", allow_reuse=True)(validate_external_url)


class Account(TypesBaseModel):
    pk: str
    username: str
    full_name: str
    is_private: bool
    profile_pic_url: HttpUrl
    is_verified: bool
    biography: Optional[str] = ""
    external_url: Optional[str] = None
    is_business: bool
    birthday: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[int] = None
    email: Optional[str] = None

    _external_url = validator("external_url", allow_reuse=True)(validate_external_url)


class UserShort(TypesBaseModel):
    pk: str
    username: Optional[str] = None
    full_name: Optional[str] = ""
    profile_pic_url: Optional[HttpUrl] = None
    profile_pic_url_hd: Optional[HttpUrl] = None
    is_private: Optional[bool] = None
    # is_verified: bool  # not found in hashtag_medias_v1
    # stories: List = [] # not found in fbsearch_suggested_profiles


class Usertag(TypesBaseModel):
    user: UserShort
    x: float
    y: float


class Location(TypesBaseModel):
    pk: Optional[int] = None
    name: str
    phone: Optional[str] = ""
    website: Optional[str] = ""
    category: Optional[str] = ""
    hours: Optional[dict] = {}  # opening hours
    address: Optional[str] = ""
    city: Optional[str] = ""
    zip: Optional[str] = ""
    lng: Optional[float] = None
    lat: Optional[float] = None
    external_id: Optional[int] = None
    external_id_source: Optional[str] = None
    # address_json: Optional[dict] = {}
    # profile_pic_url: Optional[HttpUrl]
    # directory: Optional[dict] = {}


class ReplyMessage(TypesBaseModel):
    id: str
    user_id: Optional[str] = None
    timestamp: datetime
    item_type: Optional[str] = None
    is_sent_by_viewer: Optional[bool] = None
    is_shh_mode: Optional[bool] = None
    text: Optional[str] = None
    placeholder: Optional[dict] = None


class DirectMessage(TypesBaseModel):
    id: str  # e.g. 28597946203914980615241927545176064
    user_id: Optional[str] = None
    thread_id: Optional[int] = None  # e.g. 340282366841710300949128531777654287254
    timestamp: datetime
    item_type: Optional[str] = None
    is_sent_by_viewer: Optional[bool] = None
    is_shh_mode: Optional[bool] = None
    reactions: Optional[dict] = None
    text: Optional[str] = None
    reply: Optional[ReplyMessage] = None
    placeholder: Optional[dict] = None


class DirectResponse(TypesBaseModel):
    unseen_count: Optional[int] = None
    unseen_count_ts: Optional[int] = None
    status: Optional[str] = None


class DirectShortThread(TypesBaseModel):
    id: str
    users: List[UserShort]
    named: bool
    thread_title: str
    pending: bool
    thread_type: str
    viewer_id: str
    is_group: bool


class DirectThread(TypesBaseModel):
    pk: str  # thread_v2_id, e.g. 17898572618026348
    id: str  # thread_id, e.g. 340282366841510300949128268610842297468
    messages: List[DirectMessage]
    users: List[UserShort]
    inviter: Optional[UserShort] = None
    left_users: List[UserShort] = []
    admin_user_ids: list
    last_activity_at: datetime
    muted: bool
    is_pin: Optional[bool] = None
    named: bool
    canonical: bool
    pending: bool
    archived: bool
    thread_type: str
    thread_title: str
    folder: int
    vc_muted: bool
    is_group: bool
    mentions_muted: bool
    approval_required_for_new_members: bool
    input_mode: int
    business_thread_folder: int
    read_state: int
    is_close_friend_thread: bool
    assigned_admin_id: int
    shh_mode_enabled: bool
    last_seen_at: dict

    def is_seen(self, user_id: str):
        """Have I seen this thread?
        :param user_id: You account user_id
        """
        user_id = str(user_id)
        own_timestamp = int(self.last_seen_at[user_id]["timestamp"])
        timestamps = [
            (int(v["timestamp"]) - own_timestamp) > 0
            for k, v in self.last_seen_at.items()
            if k != user_id
        ]
        return not any(timestamps)

