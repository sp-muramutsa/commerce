## PROJECT OVERVIEW
This project implements an auction site using Django, where users can create listings, place bids, add items to their watchlist, view active listings, and interact with other users through comments.

## MODELS
The application consists of the following models:
1. **AuctionListing**: Represents an auction listing with fields for title, description, starting bid, current price, image URL, category, and status.
2. **Bid**: Represents a bid placed on a listing, with fields for the user, listing, and bid amount.
3. **Comment**: Represents a comment made on a listing, with fields for the user, listing, and comment content.

## FEATURES

1. **Create Listing**
   - Users can create a new listing with a title, description, starting bid, optional image URL, and category.

2. **Active Listings Page**
   - Displays all currently active auction listings with their title, description, current price, and photo (if available).
   
3. **Listing Page**
   - Provides details about a specific listing, including title, description, current price, and optional image.
   - Signed-in users can add the item to their watchlist.
   - Signed-in users can bid on the item, with validation to ensure the bid meets criteria.
   - If the creator of the listing, the user can close the auction and declare the highest bidder as the winner.
   - If a user has won a closed auction, the page indicates so.
   - Users can add comments to the listing page, and all comments are displayed.

4. **Watchlist**
   - Signed-in users can view their watchlist, displaying all listings they have added.
   - Clicking on a listing redirects to its page.

5. **Categories**
   - Users can view a list of all listing categories.
   - Clicking on a category shows all active listings in that category.

6. **Django Admin Interface**
   - Site administrators can manage listings, comments, and bids through the Django admin interface.

## GETTING STARTED

1. **Clone the Repository**
   - Clone the repository to your local machine.

2. **Install Dependencies**
   - Install Django using pip: `pip install django`.
   - Install any additional dependencies specified in `requirements.txt`.

3. **Set Up the Database**
   - Run migrations to set up the database: `python manage.py migrate`.

4. **Run the Development Server**
   - Start the development server: `python manage.py runserver`.
   - Access the application in your browser at `http://localhost:8000`.

5. **Access the Admin Interface**
   - Log in to the Django admin interface to manage listings, comments, and bids: `http://localhost:8000/admin`.
