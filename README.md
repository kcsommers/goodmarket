# Goodmarket

## Description
Goodmarket is a website that bring people around the world together through buying and selling each others products. The exciting thing about this website, however, is that sellers and donate to their charity of choice if they sell something.

## User Stories
A user can view the main page as well as the market page which shows all the items on the market being sold. A user can login or sign up to buy or sell an item. If a user wants to sell an item they can decide to donate a portion of their earnings to a charity as well as deciding which charity to donate to. A user who wants to purchase an item can view where the seller is donating to and how much the seller is donating. Each user has a cart they can add items to. A user can navigate to their cart and view their items, the total cost, and a button to checkout their purchases.

## Wire Frames]

<img width="792" alt="screen shot 2018-08-13 at 11 44 07 pm" src="https://user-images.githubusercontent.com/34433863/44075959-5de1acbe-9f53-11e8-82e6-34ed99ade4db.png">
<img width="766" alt="screen shot 2018-08-13 at 11 44 17 pm" src="https://user-images.githubusercontent.com/34433863/44075952-59ffac7c-9f53-11e8-9ce0-59597cc43cb5.png">
<img width="776" alt="screen shot 2018-08-13 at 11 44 28 pm" src="https://user-images.githubusercontent.com/34433863/44075948-573af320-9f53-11e8-9d78-64b495032953.png">
<img width="754" alt="screen shot 2018-08-13 at 11 44 37 pm" src="https://user-images.githubusercontent.com/34433863/44075943-544d9596-9f53-11e8-8825-7a3442724c95.png">
<img width="764" alt="screen shot 2018-08-13 at 11 44 46 pm" src="https://user-images.githubusercontent.com/34433863/44075933-50830a54-9f53-11e8-8162-e986878b1f7c.png">
<img width="765" alt="screen shot 2018-08-13 at 11 44 55 pm" src="https://user-images.githubusercontent.com/34433863/44075927-4a450d36-9f53-11e8-8b0a-f0523833918f.png">
<img width="762" alt="screen shot 2018-08-13 at 11 45 04 pm" src="https://user-images.githubusercontent.com/34433863/44075920-473ce7bc-9f53-11e8-9929-8fe613837f1f.png">
<img width="766" alt="screen shot 2018-08-13 at 11 45 13 pm" src="https://user-images.githubusercontent.com/34433863/44075918-457d7298-9f53-11e8-96e7-49793386785e.png">
<img width="765" alt="screen shot 2018-08-13 at 11 45 21 pm" src="https://user-images.githubusercontent.com/34433863/44075915-4413b840-9f53-11e8-8c51-7c07c0780d07.png">


## Technologies Used
 * Python
 * Django
 * Stripe
 * CSS
 * HTML

 ## Aproach
 We decided as a group to with Django because the set up for back end is pretty straight forward. Django uses an admin pages to add data to the models and already comes with an auth which was ideal for our ecommerce site. To impliment users paying with their credit card we added stripe, A technology designed for payment processes. The type of Stripe method we used was Destination Charges. While setting up our models, we planned as much as possible to understand what kind of data we want to populate to each page. Our next step was to set up the views. We ended up making a total of 13 html pages (one of them being the base.html which is not a page that was rendered). Finally we finished up with styling. Our styling included getting all the pages coordinated with the color themes, button styles, and making the project responsive.

## Authors
 * Will Connelly
 * Kacy Sommers
 * Jacob Spade

## Acknowledgements
We would like to thank our instructors Steve Peters and Kyle Van Bergen for teaching and and inspiring us to build this project.