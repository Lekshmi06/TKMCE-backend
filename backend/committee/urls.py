from django.urls import path
from .views import (CreateCommittee,
                     ListCommittees, 
                     CommitteeDetailView,
                       generate_committee_report, 
                       AddMainCommitteeMembers, 
                       SubCommitteeCreateView,
                       AddSubcommitteeMemberView,
                       EditCommittee)

urlpatterns = [
    path('create-committee/', CreateCommittee.as_view(), name='create_committee'),
    path('committees/', ListCommittees.as_view(), name='list_committees'),
    path('add-main-committee-members/', AddMainCommitteeMembers.as_view(), name='add-main-committee-members'),
    path('committee/<int:committee_id>/subcommittee/', SubCommitteeCreateView.as_view(), name='add_sub_committee'),
    path('subcommittee/<int:subcommittee_id>/add-members/', AddSubcommitteeMemberView.as_view(), name='add-subcommittee-member'),
    path('committee-detail/<int:pk>/', CommitteeDetailView.as_view(), name='committee-detail'),
    path('report/<int:committee_id>/', generate_committee_report, name='committee_report'),
    path('edit/<int:committee_id>/', EditCommittee.as_view(), name='edit-committee'),
    path('committee-detail/<int:id>/delete/', AddMainCommitteeMembers.as_view(), name='committee-detail-delete'),

]
