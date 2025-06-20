from faker import Faker
from app.extensions import db
from app.models.user import User, UserRole
from app.models.match import Match, MatchStatus
from app.models.user_profile import User_Profile
from app.models.produce_listing import ProduceListing
from app.models.message import Message
from app.models.subscription import Subscription
from app.models.push_token import PushNotificationsToken
from app.models.bulk_upload import BulkUpload
from app.models.swipe_action import SwipeAction
from app.models.export_data import ExportData
from app.models.notification import Notification
from app.models.offer import Offer
from app.models.order import Order
from app.models.payment import Payment
from app.models.payment_gateway import PaymentGatewayLog

from app.models.pricing_history import PricingHistory
from app.models.tag_category import TagCategory
from app.models.WeeklyMarketSummary import WeeklyMarketSummary

from app.models.activity_log import ActivityLog
from app.models.admin_audit import AdminAudit
from app.models.cms_content import CMSContent
from app.models.feedback import Feedback
from app.models.geo_location import GeoLocation
from app.models.image import Image
from app.models.session import Session

import random
from datetime import datetime

fake = Faker()

def seed_users(n=10):
    users = []
    for _ in range(n):
        user = User(
            username=fake.user_name(),
            email=fake.unique.email(),
            hashed_password=fake.password(length=12),
            role=random.choice([role.value for role in UserRole]),
            is_active=fake.boolean(chance_of_getting_true=90)
        )
        users.append(user)
        db.session.add(user)
    db.session.commit()
    return users

def seed_user_profiles(users):
    profiles = []
    for user in users:
        profile = User_Profile(
            user_id=user.id,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone_number=fake.phone_number(),
            address=fake.address(),
            profile_picture=fake.image_url(),
            is_verified=fake.boolean(chance_of_getting_true=70),
            is_active=fake.boolean(chance_of_getting_true=90),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
            location=fake.city(),
            bio=fake.text(max_nb_chars=200),
            social_links=fake.url(),
            received_notifications=fake.boolean(chance_of_getting_true=80),
            favorite_products=fake.word()
        )
        profiles.append(profile)
        db.session.add(profile)
    db.session.commit()
    return profiles

def seed_produce_listings(profiles, n=20):
    listings = []
    units = ['kg', 'lbs', 'pcs', 'bunch']
    for _ in range(n):
        farmer = random.choice(profiles)
        listing = ProduceListing(
            user_id=farmer.user_id,
            farmer_id=farmer.id,
            title=fake.word().capitalize() + " " + fake.word(),
            description=fake.text(max_nb_chars=200),
            image=fake.image_url(),
            price_per_unit=round(random.uniform(1.0, 100.0), 2),
            quantity_available=random.randint(1, 1000),
            unit_of_measurement=random.choice(units),
            location=fake.city(),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year()
        )
        listings.append(listing)
        db.session.add(listing)
    db.session.commit()
    return listings

def seed_matches(profiles, listings, n=30):
    matches = []
    for _ in range(n):
        match = Match(
            buyer_id=random.choice(profiles).id,
            produce_listing_id=random.choice(listings).id,
            match_date=fake.date_time_this_year(),
            status=random.choice([status.value for status in MatchStatus])
        )
        matches.append(match)
        db.session.add(match)
    db.session.commit()
    return matches

# Additional seed functions for other models can be added here similarly

def seed_push_tokens(users, n=30):
    tokens = []
    platforms = ['iOS', 'Android']
    for _ in range(n):
        token = PushNotificationsToken(
            user_id=random.choice(users).id,
            token=fake.uuid4(),
            platform=random.choice(platforms),
            created_at=fake.date_time_this_year()
        )
        tokens.append(token)
        db.session.add(token)
    db.session.commit()
    return tokens

def seed_bulk_uploads(users, n=20):
    uploads = []
    statuses = ['pending', 'processing', 'completed', 'failed']
    for _ in range(n):
        upload = BulkUpload(
            user_id=random.choice(users).id,
            file_path=fake.file_path(depth=3),
            status=random.choice(statuses),
            created_at=fake.date_time_this_year()
        )
        uploads.append(upload)
        db.session.add(upload)
    db.session.commit()
    return uploads

def seed_offer(users, listings, n=20):
    statuses = ['pending', 'accepted', 'rejected']
    offers = []
    for _ in range(n):
        offer = Offer(
            listing_id=random.choice(listings).id,
            buyer_id=random.choice(users).id,
            offered_price=round(random.uniform(10.0, 1000.0), 2),
            quantity_requested=round(random.uniform(1.0, 100.0), 2),
            status=random.choice(statuses),
            timestamp=fake.date_time_this_year()
        )
        offers.append(offer)
        db.session.add(offer)
    db.session.commit()
    return offers

def seed_swipe_actions(users, listings, n=30):
    actions = []
    action_types = ['like', 'dislike', 'super_like']
    for _ in range(n):
        action = SwipeAction(
            user_id=random.choice(users).id,
            produce_listing_id=random.choice(listings).id,
            action_type=random.choice(action_types),
            timestamp=fake.date_time_this_year().timestamp()
        )
        actions.append(action)
        db.session.add(action)
    db.session.commit()
    return actions

def seed_export_data(users, n=20):
    exports = []
    export_types = ['csv', 'json', 'xml']
    for _ in range(n):
        export = ExportData(
            user_id=random.choice(users).id,
            export_type=random.choice(export_types),
            file_path=fake.file_path(depth=3),
            created_at=fake.date_time_this_year()
        )
        exports.append(export)
        db.session.add(export)
    db.session.commit()
    return exports

def seed_notification(users, n=20):
    notifications = []
    notification_types = ['match', 'message', 'report', 'alert', 'reminder', 'other']
    delivery_methods = ['email', 'sms', 'push', 'in_app']
    for _ in range(n):
        notification = Notification(
            user_id=random.choice(users).id,
            notification_type=random.choice(notification_types),
            delivery_method=random.choice(delivery_methods),
            content=fake.text(max_nb_chars=200),
            created_at=fake.date_time_this_year()
        )
        notifications.append(notification)
        db.session.add(notification)
    db.session.commit()
    return notifications

def seed_messages(users, matches, n=20):
    messages = []
    for _ in range(n):
        sender = random.choice(users)
        receiver = random.choice([u for u in users if u != sender])
        match = random.choice(matches)
        message = Message(
            sender_id=sender.id,
            receiver_id=receiver.id,
            content=fake.text(max_nb_chars=200),
            timestamp=int(fake.date_time_this_year().timestamp()),
            match_id=match.id
        )
        messages.append(message)
        db.session.add(message)
    db.session.commit()
    return messages

def seed_subscriptions(users, n=20):
    plans = ['Basic', 'Premium', 'Pro']
    statuses = ['active', 'cancelled', 'expired']
    subscriptions = []
    for _ in range(n):
        user = random.choice(users)
        start_date = fake.date_time_this_year()
        end_date = fake.date_time_between_dates(datetime_start=start_date)
        subscription = Subscription(
            user_id=user.id,
            plan_name=random.choice(plans),
            start_date=start_date,
            end_date=end_date,
            status=random.choice(statuses)
        )
        subscriptions.append(subscription)
        db.session.add(subscription)
    db.session.commit()
    return subscriptions

def seed_orders(users, listings, n=20):
    statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
    orders = []
    for _ in range(n):
        listing = random.choice(listings)
        buyer = random.choice(users)
        quantity = round(random.uniform(1, 100), 2)
        total_price = round(quantity * random.uniform(1.0, 100.0), 2)
        order = Order(
            listing_id=listing.id,
            buyer_id=buyer.id,
            quantity=quantity,
            total_price=total_price,
            status=random.choice(statuses),
            created_at=fake.date_time_this_year()
        )
        orders.append(order)
        db.session.add(order)
    db.session.commit()
    return orders

def seed_payments(users, orders, n=20):
    payment_methods = ['mpesa', 'paypal', 'stripe', 'bank_transfer']
    statuses = ['pending', 'completed', 'failed']
    payments = []
    for _ in range(n):
        user = random.choice(users)
        order = random.choice(orders)
        payment = Payment(
            user_id=user.id,
            amount=round(random.uniform(10.0, 1000.0), 2),
            payment_method=random.choice(payment_methods),
            status=random.choice(statuses),
            transaction_id=fake.uuid4(),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
            related_order_id=order.id,
            description=fake.sentence()
        )
        payments.append(payment)
        db.session.add(payment)
    db.session.commit()
    return payments

def seed_payment_gateway_logs(n=20):
    providers = ['mpesa', 'paypal']
    logs = []
    for _ in range(n):
        log = PaymentGatewayLog(
            provider=random.choice(providers),
            payload=fake.text(max_nb_chars=500),
            response=fake.text(max_nb_chars=500),
            timestamp=fake.date_time_this_year()
        )
        logs.append(log)
        db.session.add(log)
    db.session.commit()
    return logs

def seed_pricing_history(listings, n=20):
    histories = []
    for _ in range(n):
        listing = random.choice(listings)
        old_price = f"{round(random.uniform(1.0, 50.0), 2)} USD/kg"
        new_price = f"{round(random.uniform(1.0, 50.0), 2)} USD/kg"
        history = PricingHistory(
            listing_id=listing.id,
            price_per_unit=new_price,
            old_price_per_unit=old_price,
            new_price_per_unit=new_price,
            quantity_available=f"{random.randint(1, 1000)} kg",
            timestamp=fake.date_time_this_year()
        )
        histories.append(history)
        db.session.add(history)
    db.session.commit()
    return histories

def seed_tag_categories(n=20):
    categories = []
    for _ in range(n):
        category = TagCategory(
            name=fake.unique.word().capitalize(),
            description=fake.text(max_nb_chars=100),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year()
        )
        categories.append(category)
        db.session.add(category)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
    return categories

def seed_weekly_market_summaries(n=20):
    summaries = []
    for _ in range(n):
        start_date = fake.date_time_this_year()
        end_date = fake.date_time_between_dates(datetime_start=start_date)
        summary = WeeklyMarketSummary(
            county=fake.city(),
            week_start_date=start_date,
            week_end_date=end_date,
            demand_data=fake.text(max_nb_chars=500),
            total_sales=round(random.uniform(1000, 10000), 2),
            total_units_sold=random.randint(100, 1000),
            average_price_per_unit=round(random.uniform(1.0, 100.0), 2)
        )
        summaries.append(summary)
        db.session.add(summary)
    db.session.commit()
    return summaries

def seed_activity_logs(users, n=20):
    actions = ['login', 'logout', 'create', 'update', 'delete', 'view', 'match', 'other']
    logs = []
    for _ in range(n):
        log = ActivityLog(
            user_id=random.choice(users).id,
            action=random.choice(actions),
            description=fake.text(max_nb_chars=200),
            ip_address=fake.ipv4(),
            user_agent=fake.user_agent(),
            related_order_id=None
        )
        logs.append(log)
        db.session.add(log)
    db.session.commit()
    return logs

def seed_admin_audits(users, n=20):
    audits = []
    for _ in range(n):
        admin = random.choice(users)
        target_user = random.choice(users)
        audit = AdminAudit(
            admin_id=admin.id,
            action=fake.text(max_nb_chars=200),
            target_user_id=target_user.id,
            timestamp=fake.date_time_this_year()
        )
        audits.append(audit)
        db.session.add(audit)
    db.session.commit()
    return audits

def seed_cms_content(users, n=20):
    contents = []
    for _ in range(n):
        content = CMSContent(
            title=fake.sentence(nb_words=6),
            content=fake.text(max_nb_chars=500),
            author_id=random.choice(users).id,
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year()
        )
        contents.append(content)
        db.session.add(content)
    db.session.commit()
    return contents

def seed_feedback(users, n=20):
    feedbacks = []
    for _ in range(n):
        feedback = Feedback(
            user_id=random.choice(users).id,
            content=fake.text(max_nb_chars=500),
            rating=round(random.uniform(1, 5), 1),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year()
        )
        feedbacks.append(feedback)
        db.session.add(feedback)
    db.session.commit()
    return feedbacks

def seed_geo_locations(n=20):
    locations = []
    for _ in range(n):
        location = GeoLocation(
            latitude=random.uniform(-90, 90),
            longitude=random.uniform(-180, 180),
            address=fake.address(),
            city=fake.city()
        )
        locations.append(location)
        db.session.add(location)
    db.session.commit()
    return locations

def seed_images(n=20):
    file_types = ['image/jpeg', 'image/png', 'image/gif']
    images = []
    for _ in range(n):
        image = Image(
            url=fake.image_url(),
            description=fake.text(max_nb_chars=200),
            file_size=random.uniform(1000, 1000000),
            file_type=random.choice(file_types),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year()
        )
        images.append(image)
        db.session.add(image)
    db.session.commit()
    return images

def seed_sessions(users, n=20):
    sessions = []
    for _ in range(n):
        start_time = fake.date_time_this_year()
        end_time = fake.date_time_between_dates(datetime_start=start_time)
        duration = (end_time - start_time).total_seconds()
        session = Session(
            session_id=fake.uuid4(),
            token=fake.uuid4(),
            device_info=fake.user_agent(),
            user_id=random.choice(users).id,
            start_time=start_time,
            end_time=end_time,
            duration=duration
        )
        sessions.append(session)
        db.session.add(session)
    db.session.commit()
    return sessions

def seed_all():
    print("Seeding users...")
    users = seed_users(20)
    print("Seeding user profiles...")
    profiles = seed_user_profiles(users)
    print("Seeding produce listings...")
    listings = seed_produce_listings(profiles, 40)
    print("Seeding matches...")
    matches = seed_matches(profiles, listings, 50)
    print("Seeding push tokens...")
    push_tokens = seed_push_tokens(users, 30)
    print("Seeding bulk uploads...")
    bulk_uploads = seed_bulk_uploads(users, 20)
    print("Seeding swipe actions...")
    swipe_actions = seed_swipe_actions(users, listings, 30)
    print("Seeding export data...")
    export_data = seed_export_data(users, 20)
    print("Seeding notifications...")
    notifications = seed_notification(users, 20)
    print("Seeding offers...")
    offers = seed_offer(users, listings, 20)
    print("Seeding messages...")
    messages = seed_messages(users, matches, 20)
    print("Seeding subscriptions...")
    subscriptions = seed_subscriptions(users, 20)
    print("Seeding orders...")
    orders = seed_orders(users, listings, 20)
    print("Seeding payments...")
    payments = seed_payments(users, orders, 20)
    print("Seeding payment gateway logs...")
    payment_gateway_logs = seed_payment_gateway_logs(20)
    print("Seeding pricing history...")
    pricing_histories = seed_pricing_history(listings, 20)
    print("Seeding tag categories...")
    tag_categories = seed_tag_categories(20)
    print("Seeding weekly market summaries...")
    weekly_market_summaries = seed_weekly_market_summaries(20)
    print("Seeding activity logs...")
    activity_logs = seed_activity_logs(users, 20)
    print("Seeding admin audits...")
    admin_audits = seed_admin_audits(users, 20)
    print("Seeding CMS content...")
    cms_contents = seed_cms_content(users, 20)
    print("Seeding feedback...")
    feedbacks = seed_feedback(users, 20)
    print("Seeding geo locations...")
    geo_locations = seed_geo_locations(20)
    print("Seeding images...")
    images = seed_images(20)
    print("Seeding sessions...")
    sessions = seed_sessions(users, 20)
    print("Seeding completed.")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_all()
