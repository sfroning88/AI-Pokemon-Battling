def fetch_existing_users():
    # create Supabase client
    import os
    from supabase import create_client
    supabase_key = os.environ.get('SUPABASE_KEY')
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase = create_client(supabase_url, supabase_key)

    if supabase_key is None or supabase_url is None:
        print("ERROR: Supabase url or Supabase key was missing")
        return None

    response = (
        supabase.table("victoryroadai_users")
        .select("user_email")
        .execute()
    )
    return response.data if len(response.data) > 0 else None

def post_new_user(user_email, user_display, user_logo=None):
    # create Supabase client
    import os
    from supabase import create_client
    supabase_key = os.environ.get('SUPABASE_KEY')
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase = create_client(supabase_url, supabase_key)

    if supabase_key is None or supabase_url is None:
        print("ERROR: Supabase url or Supabase key was missing")
        return None

    user_data = {
        "user_email": user_email,
        "user_display": user_display
    }
    response = (
        supabase.table("victoryroadai_users")
        .insert(user_data)
        .execute()
    )
    return response.data if response.data else None

def post_user_avatar(user_email, image_file):
    # create Supabase client
    import os
    from supabase import create_client
    supabase_key = os.environ.get('SUPABASE_KEY')
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase = create_client(supabase_url, supabase_key)

    if supabase_key is None or supabase_url is None:
        print("ERROR: Supabase url or Supabase key was missing")
        return None

    # Create filename using email prefix
    email_base = user_email.split('@')[0]
    file_extension = os.path.splitext(image_file.filename)[1].lower()
    filename = f"{email_base}{file_extension}"
    
    # Upload to S3 bucket
    response = supabase.storage.from_("victoryroadai-avatars").upload(
        filename,
        image_file.read(),
        file_options={"content-type": image_file.content_type}
    )
    
    return filename if response else None

def fetch_avatar_url(filename):
    # create Supabase client
    import os
    from supabase import create_client
    supabase_key = os.environ.get('SUPABASE_KEY')
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase = create_client(supabase_url, supabase_key)

    if supabase_key is None or supabase_url is None:
        print("ERROR: Supabase url or Supabase key was missing")
        return None

    # Get public URL for the image
    response = supabase.storage.from_("victoryroadai-avatars").get_public_url(filename)
    return response