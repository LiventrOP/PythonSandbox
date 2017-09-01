#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Systematically search through Discord comments to find unformatted Code.

    * Look for lines ending in ;
    * Look for lines ending in )
    * Look for lines ending in { or }
    * If found, Locate the first Code Block Line
    * If found, Locate the last Code Block Line
    * RePost the message surrounded by ```csharp ```


    EXAMPLE

    ```csharp
    using UnityEngine;

    /// <summary>
    /// Class for holding Navigation variables. Used for the main game
    /// logic by PlayerNavigate to
    /// </summary>
    public class ChangeDirection
    {
        /// <summary>   The angle by which we should rotate. </summary>
        public float newAngle;
        /// <summary>   The time at which we should change direction.</summary>
        public float changeTime;

        public ChangeDirection(float _newAngle, float _changeTime)
        {
            this.newAngle = _newAngle;
            this.changeTime = _changeTime;
        }
    }
    ```
"""

import os
import re

# Keeps track of the number of instances of code-like lines
_total_lines_of_code = 0
# Holds every line as a string
_lines = []
# Keeps track of the indexes of code-like lines
_code_lines = []

_is_good_code = False


# -----------------------------------------------------------------------#
# GETPATH: GETS THE CURRENT OPERATING PATH                               #
# -----------------------------------------------------------------------#
def _get_path():  # THIS IS JUST FOR GETTING THE FILE
    """ Return the current working directory """
    return os.path.dirname(os.path.abspath(__file__)) + '/'


# Could do this in one function, and pass int the character
def _check_last_character(line_index, input_line, code_character):
    """ Check if the current line ends in the given character

    Notes:
        should check for ';', '{', '}', '(', ')'
    Args:
        (int) line_index
        (str) input_line
        (str) code_character

    Returns:
        nothing
    """
    global _total_lines_of_code
    if input_line.endswith(code_character):
        _code_lines.append(line_index)
        _total_lines_of_code += 1


def _check_semicolon(line_index, input_line):
    """
    Check if the current line ends in semicolon ;

    Args:
        (int) line_index
        (str) input_line

    Returns:
        nothing
    """
    global _total_lines_of_code
    if input_line.endswith(';'):
        _code_lines.append(line_index)
        _total_lines_of_code += 1


def _check_brackets(line_index, input_line):
    """
    Check if the current line ends in brackets { or }

    Args:
        (int) line_index
        (str) input_line

    Returns:
        nothing
    """
    global _total_lines_of_code
    if input_line.endswith('{') or input_line.endswith('}'):
        _code_lines.append(line_index)
        _total_lines_of_code += 1


def _check_parenthesis(line_index, input_line):
    """
    Check if the current line ends in brackets )

    Args:
        (int) line_index
        (str) input_line

    Returns:
        nothing
    """
    global _total_lines_of_code
    # Only cheking for closing now
    if input_line.endswith(')'):
        _code_lines.append(line_index)
        _total_lines_of_code += 1


def _is_bad_code():
    """ Checks if we have enough crieria to be bad code

    Note:
        * Currently checks for 5 or more code-like lines *

    Returns:
        True or False
    """
    if _total_lines_of_code >= 5:
        return True
    else:
        return False


def _get_first_code_line():
    """ Get the minimum value in code_lines

    Returns:
        (int) min value in code_lines
    """
    return min(_code_lines)


def _get_last_code_line():
    """ Get the maximum value in code_lines

    Returns:
        (int) max value in code_lines
    """
    return max(_code_lines) + 2


def check_message_for_code(in_lines):
    """ Checks a given multi-line string object for code-like structre

    Args:
        (list) in_lines

    Returns:
        nothing
    """
    global _is_good_code
    # Loop through every line, and track its index
    for index, line in enumerate(in_lines):
        # Remove all tabs and newlines and bad stuff
        line = re.sub('\s+', '', line)
        # Check if this is formatted code.
        if line.find('```') >= 0:
            print(line.find('```'))
            print("This code is fine, probably")
            _is_good_code = True
            return
        # Check for code-like stuffs :D
        else:
            _check_last_character(index, line, ';')
            _check_last_character(index, line, '{')
            _check_last_character(index, line, '}')
            _check_last_character(index, line, ')')

# Get the message somehow (bot stuff)

# Store the message in some object (lines)

# Call check_message_for_code(lines)

# If the file exists
if os.path.isfile(_get_path() + 'badcode.txt'):
    # Open the file
    with open(_get_path() + 'badcode.txt') as input_file:
        # Store each line in an array
        _lines = input_file.readlines()
        # Not necessary, but here we are :/
        if _lines:
            check_message_for_code(_lines)


# If we are, in fact, bad code, lets fix it
if _is_bad_code() and not _is_good_code:
    # Get the first and last line of code
    first_line = _get_first_code_line()
    last_line = _get_last_code_line()

    # Insert formatting stuff around the code block
    _lines.insert(first_line, '```csharp\n')
    _lines.insert(last_line, '\n```\n')

    # Set the outpout file name
    fileName = "Discord/good_code.txt"

    # Open the output file
    output_file = open(fileName, 'w')

    # Write all lines to file
    for l in _lines:
        output_file.write(l)
    output_file.close()
