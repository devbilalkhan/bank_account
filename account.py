# account.py

import numbers
from datetime import datetime, timedelta
from itertools import count
import re

class TimeZone:
  """
  TimeZone class to represent a time zone.

  Attributes:
      name (str): Time zone ka naam 
      offset_hours (int, optional): The offset in hours from UTC. Defaults to 0.
      offset_minutes (int, optional): The offset in minutes from UTC. Defaults to 0.
  """

  def __init__(self, name, offset_hours= 0, offset_minutes = 0):
    
    # Name validation
    # timezone ka naam khali nahi hona chahiye warna user to error bhej dain    
    if name is None or len(str(name).strip()) == 0:
      raise ValueError("Timezone cannot be empty. Please enter a timezone name.")
    
    # timezone instance private attribute
    self._name = str(name).strip()
    
    # offset validation
    if not isinstance(offset_hours, numbers.Integral):
      raise ValueError("Offset_hours must be a number.")
    
    if not isinstance(offset_minutes, numbers.Integral):
      raise ValueError("Offset minutes must be number.")
    
    if offset_minutes < -59 or offset_minutes > 59:
      raise ValueError("Offset minutes must be between -59 and 59 (inclusive).")
    
    # Check kerain kay offset hours -12 hours aur 14 kay limit kay ander ho
    # offset aik local variable sirf verfication kay maqsad kay liye
    offset = timedelta(hours=offset_hours, minutes=offset_minutes)
    if offset < timedelta(hours=-12, minutes=0) or offset > timedelta(hours=14, minutes=0):
      raise ValueError("Offset must be between -12:00 and +14:00 range." )
    
    # Psuedo properties 
    self._offset_hours = offset_hours
    self._offset_minutes = offset_minutes
    self._offset = offset
    
  # Name property getter - read only property
  @property 
  def name(self):
    return self._name
 
 # Offset property getter - read only property
  @property
  def offset(self):
    return self._offset
  
  # Yeh function check karta hai ke kya 'self' aur 'other' same hain ya nahi.
  # Pehle yeh check karta hai ke kya 'other' ka instance 'TimeZone' hai ya nahi.
  # Agar 'other' 'TimeZone' ka instance hai, toh phir yeh check karta hai ke kya 'self' aur 'other' ke 'name', 'offset' aur 'minutes' same hain ya nahi.
  # Agar yeh sab same hain, toh function 'True' return karta hai, warna 'False' return karta hai.
  def __eq__(self, other):
    if not isinstance(other, TimeZone):
          return False
    return (self.name == other.name and 
            self.offset_hours == other.hours and 
            self._offset_minutes == other.minutes)
  
  # Yeh function 'self' object ki representation return karta hai.
  # Yeh representation 'self' object ke 'name', 'offset_hours' aur 'offset_minutes' attributes ko include karta hai.
  # Yeh representation aik string hai jo 'f-string' format mein hai.
  def __repr__(self):
    return (
      f"Timezone(name={self._name}), "
      f"offset={self._offset_hours}, "
      f"offset={self._offset_minutes} "
    )
    
# Bank account  
class Account:
  """
  Account class banks accounts kay liye
  
  Attributes:
    first_name: (str) Account rakhne wale ka pehla naam
    last_name: (str) Account rakhne wale ka family naam 
    account_number: (str) Account ka number 
    timeZone: (TimeZone | optional) apni pasand ka timezone 
  
  """
  
  # Unique counter - class level attribute
  # Har transaction ke liye unique counter
  transaction_counter = count(100)  
  # interst rate - class level private attribute
  _interest_rate = 0.05
  
  # TODO: Iss aik behtar method say implement kernge jise ENUM kaha jata hai. 
  # transaction codes 
  _transaction_codes = {
    'deposit': 'D',
    'withdraw': 'W',
    'interest': 'I',
    'rejected': 'X'
  }
  
  def __init__(self, account_number, first_name, last_name, 
               timeZone=None, initial_balance=0):
    # Account holder ka pehla naam
    self.first_name = first_name
    # Account holder ka aakhri naam
    self.last_name = last_name
    # Account number, private attribute
    self._account_number = account_number    
    # Account ka balance, private attribute
    self._balance = float(initial_balance)
    
    # Agar timeZone provide nahi kiya gaya to default 'UTC' set karo
    if timeZone == None:     
      timeZone = TimeZone('UTC', 0, 0)
    # Account holder ka timeZone
    self.timeZone = timeZone
    
  @property 
  def account_number(self):
    # Private account number attribute wapis karo
    return self._account_number
  
  @property 
  def first_name(self):
    """ Pehla naam hasil karo"""
    return self._first_name
  
  @first_name.setter 
  def first_name(self, value):
    # Pehla naam set karo
    self.validate_and_set_name('_first_name', value, 'Pehla Naam')
    
  @property 
  def last_name(self):
    """ Aakhri naam hasil karo"""
    return self._last_name
  
  @last_name.setter 
  def last_name(self, value):         
    # Aakhri naam set karo
    self.validate_and_set_name('_last_name', value, "Aakhri Naam")
  
  @property 
  def balance(self):
    # Account ka balance hasil karo
    return self._balance
  
  @classmethod 
  def get_interest_rate(cls):
    """ Interest rate hasil karo"""
    return getattr(cls, 'interest_rate')
  
  @classmethod 
  def set_interest_rate(cls, value):
    # validation
    if not isinstance(value, numbers.Real):
      raise ValueError("value must be a real number.")
    
    if value < 0:
      raise ValueError("value must not be negative.")    
    setattr(cls, "_interest_rate", value)
                         
  @property
  def timeZone(self):
    """ Time zone hasil karo"""
    return getattr(self, '_timeZone', None)
  
  @timeZone.setter
  def timeZone(self, value):    
    # Agar timeZone TimeZone object nahi hai to error raise karo
    if not isinstance(value, TimeZone):
      raise ValueError("TimeZone must be a TimeZone object")
    else:
      # timeZone set karo
      setattr(self, '_timeZone', value)
  
  def validate_and_set_name(self, attr_name, value, field_title):
    # Naam ka pattern check karo
    name_pattern = re.compile(r"^[A-Za-z'-]+(?: [A-Za-z'-]+)*$") 
    # Agar naam ki length 0 ya 30 se zyada hai to error raise karo
    if value is None or len(str(value).strip()) == 0  or len(value) > 30:
      raise ValueError(f'{field_title} must be greater than 1 and at most 30 characters')
    # Agar naam mein invalid characters hain to error raise karo
    if not name_pattern.match(value):
      raise ValueError(f"{field_title} contains invalid characters. Only letters, - and ' are allowed")      
    # Naam set karo
    setattr(self, attr_name, value)
    
  # Har naye transaction ke liye naya id generate karo
  def next(self):
    next_transaction_id = next(Account.transaction_counter)
    return next_transaction_id