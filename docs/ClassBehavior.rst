.. currentmodule:: swagrinth

Class Behavior
=============

-------------

.. note::

    The only real reason why you'd want to manually instance any data classes is for the sending of data to modrinth, the ability to do so has yet to be
    implemented. Feel free to ignore this part.

.. note::

    This information applies only to the Data Classes, not to Client or any exception classes

Swagrinth Data classes all share unique behavior  which is aimed at optimizing and simplifying usage internally and for the end user.

Data classes do not take any parameters when instanced, instead attributes are set using the contents of `kwargs`.
Attributes will be set to default values if a key in kwargs by the same name is absent. Any extra objects in `kwargs` are ignored.

.. code-block:: python3

    init_args = {'slug' : 'example', 'title' : 'Example Project', 'neat_attr' : 'Cool Value!!'}
    cool_new_project = Project(**init_args)

    print(cool_new_project.slug) # Prints 'example'
    print(cool_new_project.title) # Prints 'Example Project'
    print(cool_new_project.description) # Prints ''
        # Wasn't givin in the kwargs, instead it was set to it's default. 
    print(cool_new_project.neat_attr) # Raises AttributeError

Attempting to set an attribute using a value of a type it doesn't expect raises ObjectInitError

.. code-block:: python3

    modified_user = User(**{'username' : 1234})
    # User's attribute 'username' is expected to be a string, 
    # because the value listed in the kwargs is a int, ObjectInitError is raised

When a attribute expects/defaults to another object, giving an object *or* giving a nested dictionary in `kwargs` will work.

.. code-block:: python3

    fake_dict = {'id' : 'fake-license', 'title' : 'Fake Example License'}

    fake_license = License(**fake_dict)
    project_with_license = Project(**{'license' : fake_license}) # This works

    project_2_with_license = Project(**{'license' : fake_dict}) # This will also work

Passing a key with a value of ``None`` is the same as not listing the key at all

.. code-block:: python3

    tiny_dict = {'display_name' : None}

    empty_user = User(**tiny_dict)

    print(empty_user.display_name) # This attribute fell back on it's default. Prints ''



    


