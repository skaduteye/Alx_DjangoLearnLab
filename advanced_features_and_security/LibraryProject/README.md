# Advanced Features and Security - Django Project

## Permissions and Groups Setup

This project demonstrates how to use Django's permissions and groups to control access to model actions.

### Custom Permissions
- Defined in `bookshelf/models.py` for the `Book` model:
  - `can_view`: Can view book
  - `can_create`: Can create book
  - `can_edit`: Can edit book
  - `can_delete`: Can delete book

### Groups
- Create groups in Django admin:
  - Editors: Assign `can_edit`, `can_create`
  - Viewers: Assign `can_view`
  - Admins: Assign all permissions
- Add users to groups as needed

### Views
- All book actions are protected with `@permission_required` decorators in `bookshelf/views.py`:
  - `view_books`: Requires `can_view`
  - `create_book`: Requires `can_create`
  - `edit_book`: Requires `can_edit`
  - `delete_book`: Requires `can_delete`

### Testing
- Assign users to groups and verify access to each view
- Only users with the correct permissions can perform actions

---
For more details, see comments in `bookshelf/views.py`.
