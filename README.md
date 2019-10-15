Creating a New Siteflavor
=========================

## Templates, Directories, Views and Models

#### Create Directory
In your positron project, add a directory to the siteflavor directory named after your domain.
For this example chocolatechip will be out directory name.

Copy everything from the boilerplate _except the gitignore file_ into your new directory. 

#### Rename Files and Directories
* Rename the in /templates/ rename the boilerplate directory to the chocolatechip
* Rename each file in this directory to reflect the new siteflavor (chocolate_chip_about_page.html)

#### Update Views and Models
* BoilerplateSchoolView > ChocolateChipSchoolView
* BoilerplateSearchSchools > ChocolateChipSearchSchools
* ContactFormView needs an updated template path
* Rename all models, be sure to reference all 

#### Update urls.py
Update imports or siteflavor specific views and url patterns

## Positron Siteflavor Settings

#### chocolatechip/settings.py
* INSTALLED_APPS = (‘siteflavor.chocolatechip’,...,...,...)
* WAGTAIL_SITE_NAME = 'Chocolate Chip'
* ROOT_URLCONF = 'siteflavor.chocolatechip.urls'

#### MANIFEST.in
Add the new siteflavor’s static and template directories to MANIFEST.in
recursive-include siteflavor/chocolatechip/static *
recursive-include siteflavor/chocolatechip/templates *

#### base.py
* Add you siteflavor below others CHOCOLATE_CHIP = ‘chocolatechip’
* Add CHOCOLATE_CHIP to FLAVORS
* SITE_FLAVOR = os.environ.get('POSITRON_SITE_FLAVOR', CHOCOLATE_CHIP)
* Updating SITE_FLAVOR allows you run the siteflavor locally and collect it’s static files. Don’t commit this change.

#### PyCharm Django server Configuration
Update POSITRON_SITE_FLAVOR in your Environment variables

#### Logfile
You’ll need to create a log file with read and write permissions
* `sudo touch /var/log/positron/positron-chocolatechip.log`
* `sudo chmod 777 /var/log/positron/positron-chocolatechip.log`

#### Collect Static
* First, delete the directory called ‘static’ within positron/positron.
* This is where the static files for your siteflavor will be placed when you run the management command ‘collectstatic’
* If you don’t delete the directory, the collectstatic command will just append your siteflavor’s static files to the existing files in ‘static’.

Next, in a terminal window
* `workon positron`
* `./manage.py collectstatic`

Make those migrations
* `./manage makemigrations`
* `./manage migrate`

At this point you should be able to run positron with your siteflavor, but we’ll need to update some wagtail settings to see it in action.

## Wagtail Settings
#### Add a Page
We’ll be adding a new Site to wagtail, but we’ll need an index page for the Site to point to.
* Visit /cms/pages on your server (127.0.0.1:8111/cms/pages/)
* Add Child Page
* Select Chocolate chip index page
* Give it a title of Chocolate Chip
* Click the up arrow next to ‘Save Draft’ and click ‘Publish’

#### Create a Site
* Visit Settings > Sites
* Click Add Site
* Local Settings
  * Hostname: localhost or 127.0.0.1
  * Port: whatever port your local positron server is using, for me it’s 8111
  * Site name: Chocolate Chip
  * Select the root page you just created.
  * Leave ‘Is default site’ unchecked
* Production Settings
  * Hostname: www.chocolatechip.com
  * Port: 80
  * Site name: Chocolate Chip
  * Select the root page you just created.
  * Leave ‘Is default site’ unchecked

#### Create Pages in Wagtail
In your models, there are a number of predefined pages provided by the boilerplate.
* Select one of these pages and fill out the required fields.
  * About
  * Blog Index
  * The BlogPage is accessible as a child page to Blog Index
  * Contact
  * Index (what you used for your root page)
  * Landing Page
  * Page (this is a generic page, used for things like Privacy Policy and Terms of Use)
  * School and SchoolPage, are used for the School Directory, don’t worry about those.

_If you are going to add the page to a menu, you must check the ‘Show in menus’ option in the Promote tab. Otherwise it will not show up when you add the page to a menu._

#### Create Menus for the Header or Footer in Wagtail
* Visit Settings > Flat Menus > Add Flat Menu
  * Name: Whatever makes sense (Footer Menu, Main Menu, Social Menu)
  * Site: Chocolate Chip
  * Handle: main_menu, footer_menu, social_menu
  * Heading: leave it blank

* Footer and Main Menu items are straight forward enough.

* For social menu items follow this pattern
  * Link to custom url: https://www.facebook.com/collegeoverview/
  * Link Text: facebook
  * Link handle: facebook

The social platforms supported by our css are:
facebook, instagram, twitter, medium, google-plus

If you want to add more support, just add a new class in common/static/scss/common/components/_icons.scss

Customizing a Siteflavor
========================
#### Templates
You’ll notice that many templates in your new siteflavor simply extend a template in the common directory. This prevents us from duplicating code, but still allows for customization using Django’s template block tags.

We implemented wherever it made sense. For an example of how this works, check out the external directory in your new siteflavor’s templates. Since the multistep external controllers point to the current siteflavor’s submission forms, you can totally overwrite the form if you need.

#### Styles
There are a large amount of scss variables available to adjust colors, fonts, images, and layouts. 

Only write new styles if you’re sure there isn’t a variable you can overwrite to achieve the desired result.

#### Hero Images
Simply define the image path in the correct variables.

You’ll be saving at least 4 images to handle various screen sizes.
Check the defaults.scss file in common to find your options.

For example the directory page uses these:
* $directory__hero--hero--480w
* $directory__hero--hero--768w
* $directory__hero--hero--1200w
* $directory__hero--hero--1983w

Edge Case Example:

For MedicalCareersDirect we had to add an additional variable and media query for a wider screen. The image we were using didn’t scale well beyond a certain point.
Check out core/directory/directory_page.scss to see how to handle that situation.
The media queries are at the bottom.

You’ll probably want to update these as well
* $multistep__shortform-modal--logo-width
* $multistep__shortform-modal--logo-height

Since logos can vary quite widely, there are style definitions defined in each siteflavor.
You’ll find those in main.scss

#### Static Assets
##### Favicon
Save a 48x48 png file containing your logo mark and a transparent background.
Upload to a favicon converter like the one below.
https://favicon.io/favicon-converter/

##### Logo
Base64 encode your svg and update the logo variables found in _defaults.scss by replacing everything after 'data:image/svg+xml;base64,’
https://www.mobilefish.com/services/base64/base64.php
