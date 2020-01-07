"""
    This file is part of Gig-o-Matic

    Gig-o-Matic is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from django.db import models
from member.models import Member
from band.models import Band

class Gig(models.Model):
    title = models.CharField(max_length=200)
    band = models.ForeignKey(Band, related_name="gigs", on_delete=models.CASCADE)

    # todo when a member leaves the band must set their contact_gigs to no contact. Nolo Contacto!
    contact = models.ForeignKey(Member, null=True, related_name="contact_gigs", on_delete=models.SET_NULL)
    details = models.TextField(null=True, blank=True)
    setlist = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    date = models.DateField()
    enddate = models.DateField(null=True, blank=True)

    calltime = models.TimeField(null=True, blank=True)
    settime = models.TimeField(null=True, blank=True)
    endtime = models.TimeField(null=True, blank=True)

    address = models.TextField(null=True, blank=True)
    dress = models.TextField(null=True, blank=True)
    paid = models.TextField(null=True, blank=True)
    postgig = models.TextField(null=True, blank=True)

    leader = models.ForeignKey(Member, blank=True, null=True, related_name="leader_gigs", on_delete=models.SET_NULL)

    # todo manage these
    # trueenddate = ndb.ComputedProperty(lambda self: self.enddate if self.enddate else self.date)
    # sorttime = ndb.IntegerProperty( default=None )

    class StatusOptions(models.IntegerChoices):
            UNKNOWN = 0
            CONFIRMED = 1
            CANCELLED = 2
            ASKING = 3
    status = models.IntegerField(choices=StatusOptions.choices, default=StatusOptions.UNKNOWN)

    @property
    def is_canceled(self):
        self.status=StatusOptions.CANCELLED

    @property
    def is_confirmed(self):
        self.status=StatusOptions.CONFIRMED

    # todo archive
    # archive_id = ndb.TextProperty( default=None )
    # is_archived = ndb.ComputedProperty(lambda self: self.archive_id is not None)

    is_private = models.BooleanField(default=False )    

    # todo what's this?
    # comment_id = ndb.TextProperty( default = None)

    creator = models.ForeignKey(Member, null=True, related_name="creator_gigs", on_delete=models.SET_NULL)

    invite_occasionals = models.BooleanField(default=True)
    was_reminded = models.BooleanField(default=False)
    hide_from_calendar = models.BooleanField(default=False)
    default_to_attending = models.BooleanField( default=False )

    rss_description = models.TextField( null=True, blank=True )
    trashed_date = models.DateTimeField( blank=True, null=True )

    @property
    def is_in_trash(self):
        return self.trashed_date is not None

    def __str__(self):
        return self.title
