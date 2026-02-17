# 🦇 Users CRUD over Groups — Feature Breakdown

A sequential breakdown of the **Warden's Command Center** feature, component by component, in the exact order they execute when a request hits the server.

<br>

---

## 🔗 Component 1: The Front Gate — `urls.py`

```python
router.register('user-groups', views.UserGroupViewSet, basename='user-groups')
```

**What it does**: This is the **address plate** on the building. When someone hits `/api/v1/default-router/user-groups`, Django's router knows to forward the request to `UserGroupViewSet`. While `ModelViewSet` auto-generates all 5 CRUD URLs, we lock the door using `http_method_names = ['get', 'patch']` — only allowing what the Warden actually needs:

| Method | URL | Action | Status |
|--------|-----|--------|--------|
| `GET` | `/user-groups` | `.list()` — all users | ✅ Allowed |
| `GET` | `/user-groups/16` | `.retrieve()` — single user | ✅ Allowed |
| `PATCH` | `/user-groups/16` | `.partial_update()` — edit groups | ✅ Allowed |
| `POST` | `/user-groups` | `.create()` — new user | 🚫 `405 Method Not Allowed` |
| `PUT` | `/user-groups/16` | `.update()` — full replace | 🚫 `405 Method Not Allowed` |
| `DELETE` | `/user-groups/16` | `.destroy()` — remove user | 🚫 `405 Method Not Allowed` |

> **Why block POST?** User registration is handled by Djoser (`/api/auth/users/`). This endpoint is only for managing *existing* users' groups.
> **Why block DELETE?** Nuking a user from the database is too destructive. The Warden should demote, not destroy.

<br>

---

## 🛡️ Component 2: The Security Gate — `permissions.py`

```python
class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
```

**What it does**: Before the request even touches the ViewSet logic, **this bouncer checks your badge**. It asks one question: *"Are you a superuser?"* If `False` → instant `403 Forbidden`. If `True` → you may pass.

**Key detail**: This is different from `IsSecurityStaff` (which checks group membership). `IsSuperAdmin` checks the `is_superuser` flag on the Django User model — a boolean that only `createsuperuser` or another superuser can set.

<br>

---

## 📦 Component 3: The Brain — `UserGroupViewSet` in `views.py`

```python
class UserGroupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdmin]
```

**What it does**: This is the **command room** itself. Three key configuration lines:

- `queryset = User.objects.all()` → "I work with **every** user in `auth_user` table"
- `serializer_class = UserSerializer` → "I use this translator to convert DB rows ↔ JSON"
- `permission_classes = [IsSuperAdmin]` → "Only super admins get past the door"

Because it extends `ModelViewSet`, it inherits **all 5 CRUD actions** automatically. You didn't write a single `def list()` or `def retrieve()` — Django gives you those for free.

<br>

---

## 🔍 Component 4: The Intelligent Filter — `get_queryset()` override

```python
def get_queryset(self):
    queryset = super().get_queryset()
    group_name = self.request.query_params.get('group')
    if group_name:
        queryset = queryset.filter(groups__name=group_name)
    return queryset
```

**What it does**: This is the **smart search engine**. When the Warden calls:

- `GET /user-groups` → No filter → returns **all 21 users**
- `GET /user-groups?group=Medical+Staff` → Filters → returns **only the 6 doctors**

The magic is `groups__name` — this is Django's ORM doing a **reverse lookup** across the many-to-many relationship between `User` and `Group`. In SQL terms, it's doing a `JOIN` on the `auth_user_groups` junction table.

<br>

---

## 🔄 Component 5: The Promotion Engine — `perform_update()`

```python
def perform_update(self, serializer):
    serializer.save()
```

**What it does**: When the Warden sends `PATCH {"groups": ["Security Staff"]}`, this method triggers. It looks simple, but the heavy lifting happens inside the serializer (next component). This is the hook where you *could* add extra logic like logging or notifications.

<br>

---

## 🔐 Component 6: The Translator — `UserSerializer` in `serializers.py`

```python
class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']
```

**What it does**: This is the **translator** between your database and JSON. Two critical things:

1. **`SlugRelatedField`**: Instead of making the Warden send `{"groups": [3]}` (cryptic ID), he can send `{"groups": ["Medical Staff"]}` (human-readable name). The `slug_field='name'` says *"look up the Group by its `name` column"*.

2. **`many=True`**: A user can belong to **multiple** groups. So `["Medical Staff", "Security Staff"]` is valid — dual clearance.

**When reading** → converts DB group objects to `["Medical Staff"]`
**When writing** → looks up `Group.objects.get(name="Medical Staff")` and links it to the user via the many-to-many table.

<br>

---

## 📊 The Full Request Flow

```
Client Request (PATCH /user-groups/16 {"groups": ["Security Staff"]})
        │
        ▼
   ┌─────────┐
   │ urls.py  │  → Routes to UserGroupViewSet
   └────┬─────┘
        ▼
   ┌─────────────┐
   │ IsSuperAdmin │  → Checks is_superuser flag (403 if not)
   └────┬─────────┘
        ▼
   ┌──────────────────┐
   │ UserGroupViewSet  │  → Calls .partial_update() (inherited from ModelViewSet)
   └────┬──────────────┘
        ▼
   ┌───────────────┐
   │ UserSerializer │  → Validates "Security Staff" exists in Group table
   │                │  → Maps it to the user's groups (M2M)
   └────┬──────────┘
        ▼
   ┌───────────────┐
   │ perform_update │  → serializer.save() writes to DB
   └────┬──────────┘
        ▼
   Response: 200 {"id": 16, "username": "JohnDoe", "groups": ["Security Staff"]}
```
