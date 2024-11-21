from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Committe, CommitteeDetails, SubCommittee, Employee
from .serializers import CommitteSerializer, CommitteeDetailsSerializer, SubCommitteeSerializer, SubCommitteeSerializerForFetch
from django.shortcuts import get_object_or_404


import logging
logger = logging.getLogger(__name__)

from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CommitteSerializer, SubCommitteeSerializer, CommitteeDetailsSerializer, CommitteSerializerForFetch


from django.http import HttpResponse
from django.template.loader import render_to_string

class CreateCommittee(APIView):
    def post(self, request):
        serializer = CommitteSerializer(data=request.data)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'error': 'Committee validation failed.',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        



class AddMainCommitteeMembers(APIView):
    def post(self, request):
        committee_id = request.data.get("committee_id")
        members = request.data.get("members", [])

        # Check if committee exists
        try:
            committee = Committe.objects.get(id=committee_id)
        except Committe.DoesNotExist:
            return Response(
                {"error": "Committee not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Add each member to CommitteeDetails
        errors = []
        for member in members:
            serializer = CommitteeDetailsSerializer(data={
                "committee_id": committee_id,
                "employee_id": member.get("employee_id"),
                "role": member.get("role"),
                "score": member.get("score"),
                  # Associate member with committee
            })
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append({
                    "employee_id": member.get("employee_id"),
                    "errors": serializer.errors
                })

        if errors:
            return Response(
                {"error": "Some members failed validation.", "details": errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"message": "Main committee members added successfully."}, status=status.HTTP_201_CREATED)
    
    def delete(self, request,id):
        committee_detail_id = request.data.get("id")

        # Check if the CommitteeDetails entry exists
        try:
            committee_detail = CommitteeDetails.objects.get(id=id)
            committee_detail.delete()  # Remove the committee member entry
        except CommitteeDetails.DoesNotExist:
            return Response(
                {"error": "Committee member not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({"message": "Member removed successfully."}, status=status.HTTP_204_NO_CONTENT)


class SubCommitteeCreateView(APIView):
    def post(self, request, committee_id):
        try:
            committee = Committe.objects.get(id=committee_id)
        except Committe.DoesNotExist:
            return Response({"error": "Committee not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create a new SubCommittee instance
        serializer = SubCommitteeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(committee_id=committee)  # Set the committee foreign key
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddSubcommitteeMemberView(APIView):
    def post(self, request, subcommittee_id):
        # Check if the subcommittee exists
        try:
            subcommittee = SubCommittee.objects.get(id=subcommittee_id)
        except SubCommittee.DoesNotExist:
            return Response({"error": "Subcommittee not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if 'members' key is in request data
        if 'members' not in request.data:
            return Response({"error": "No members data provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and validate each member's data
        for member in request.data['members']:
            serializer = CommitteeDetailsSerializer(data=member)
            if serializer.is_valid():
                serializer.save(subcommittee_id=subcommittee)  # Save with the associated subcommittee
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Members added successfully"}, status=status.HTTP_201_CREATED)



class ListCommittees(APIView):
    def get(self, request):
        # Fetch all committees
        committees = Committe.objects.all()
        serializer = CommitteSerializerForFetch(committees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#edit---------------------    
class EditCommittee(APIView):
    def put(self, request, committee_id):
        committee = get_object_or_404(Committe, id=committee_id)
        serializer = CommitteSerializer(committee, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Committee validation failed.',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)    

class CommitteeDetailView(APIView):
    def get(self, request, pk):
        try:
            # Fetch the specific committee by ID
            committee = Committe.objects.get(id=pk)
            serializer = CommitteSerializerForFetch(committee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Committe.DoesNotExist:
            return Response({"error": "Committee not found"}, status=status.HTTP_404_NOT_FOUND)


def generate_committee_report(request, committee_id):
    # Create an instance of the CommitteeDetailView
    detail_view = CommitteeDetailView()
    response = detail_view.get(request, committee_id)
    receiver_name = request.GET.get('receiver_name')
    role = request.GET.get('role')
    if response.status_code == status.HTTP_200_OK:
        committee_data = response.data

        # Prepare the context with the necessary data
        context = {
            'order_number': committee_data.get('order_number'),
            'committe_name': committee_data.get('committe_Name'),
            'order_date': committee_data.get('order_date'),
            'order_text': committee_data.get('order_Text'),
            'order_description': committee_data.get('order_Description'),
            'committe_expiry': committee_data.get('committe_Expiry'),
            'main_members': committee_data.get('main_committee_members'),
            'sub_committees': committee_data.get('sub_committees'),
            'role': role,
            'receiver_name': receiver_name,
            'is_pdf': True,  # Flag to indicate PDF rendering
        }

        # Render the HTML template with the context
        html = render_to_string('committee_report_template.html', context)
        return HttpResponse(html)

        # Create a PDF response
        
 #------------------------------------------------------------------
#  response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = f'attachment; filename="committee_report_{committee_id}.pdf"'
        # Generate PDF
        # pisa_status = pisa.CreatePDF(html, dest=response)

        # # Check for errors
        # if pisa_status.err:
        #     return HttpResponse('We had some errors <pre>' + html + '</pre>')

        # return response
        #------------------------------------------------------------------
    else:
        return HttpResponse('Committee not found', status=404)
    

   