from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
import json
# views.py
from django.shortcuts import get_object_or_404
from .models import Drug, Manufacturer, Generic, Indication, DosageForm, DrugClass

def drug_list(request):
    drugs = Drug.objects.all()

    # Filtering
    name_filter = request.GET.get('name', '')
    generic_filter = request.GET.get('generic', '')
    drug_class_filter = request.GET.get('drug_class', '')
    dosage_form_filter = request.GET.get('dosage_form', '')

    if name_filter:
        drugs = drugs.filter(name__icontains=name_filter)
    if generic_filter:
        drugs = drugs.filter(generic__generic_name__icontains=generic_filter)
    if drug_class_filter:
        drugs = drugs.filter(generic__drug_class__icontains=drug_class_filter)
    if dosage_form_filter:
        drugs = drugs.filter(dosage_form_id__in=DosageForm.objects.filter(dosage_form_name__icontains=dosage_form_filter).values('id'))

    # Get filter options
    generics = Generic.objects.all()
    drug_classes = DrugClass.objects.all()
    dosage_forms = DosageForm.objects.all()

    return render(request, 'drug_list.html', {
        'drugs': drugs,
        'generics': generics,
        'drug_classes': drug_classes,
        'dosage_forms': dosage_forms,
        'name_filter': name_filter,
        'generic_filter': generic_filter,
        'drug_class_filter': drug_class_filter,
        'dosage_form_filter': dosage_form_filter,
    })


def drug_list_json(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))

    name = request.GET.get('name', '')
    generic = request.GET.get('generic', '')
    drug_class = request.GET.get('drug_class', '')
    dosage_form = request.GET.get('dosage_form', '')

    drugs = Drug.objects.select_related('generic').all()

    # Apply filters
    if name:
        drugs = drugs.filter(name__icontains=name)
    if generic:
        drugs = drugs.filter(generic__generic_name__icontains=generic)
    if drug_class:
        drugs = drugs.filter(generic__drug_class__icontains=drug_class)
    if dosage_form:
        drugs = drugs.filter(dosage_form__dosage_form_name__icontains=dosage_form)

    total = drugs.count()

    # Pagination
    drugs_page = drugs[start:start+length]

    data = []
    for drug in drugs_page:
        data.append({
            'name': drug.name,
            'generic': drug.generic.generic_name if drug.generic else 'N/A',
            'strength': drug.strength or 'N/A',
            'drug_type': drug.drug_type or 'N/A',
            'package_size': drug.package_size or 'N/A',
            'actions': f'''
                <button class="btn btn-info btn-sm view-details" 
                        data-id="{drug.id}">
                    View Details
                </button>
            '''
        })

    return JsonResponse({
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': data
    })

def get_drug_details(request, drug_id):
    """
    Ajax endpoint to get drug details with related models
    """
    try:
        # Get the drug with related generic data
        drug = get_object_or_404(Drug.objects.select_related('generic'), id=drug_id)
        
        # Initialize response data
        data = {
            'id': drug.id,
            'name': drug.name,
            'size': drug.size,
            'strength': drug.strength,
            'package_container': drug.package_container,
            'package_size': drug.package_size,
            'drug_type': drug.drug_type,
            'sku': drug.sku,
        }
        
        # Get Generic information
        if drug.generic:
            generic = drug.generic
            data.update({
                'generic': generic.generic_name,
                'monograph_link': generic.monograph_link,
                'indication_desc': generic.indication_description,
                'pharmacology': generic.pharmacology_description,
                'dosage': generic.dosage_description,
                'administration': generic.administration_description,
                'interaction': generic.interaction_description,
                'contraindications': generic.contraindications_description,
                'side_effects': generic.side_effects_description,
                'pregnancy': generic.pregnancy_lactation_description,
                'precautions': generic.precautions_description,
                'therapeutic_class': generic.therapeutic_class_description,
                'pediatric_usage': generic.pediatric_usage_description,
                'overdose_effects': generic.overdose_effects_description,
                'duration_treatment': generic.duration_treatment_description,
                'reconstitution': generic.reconstitution_description,
                'storage_conditions': generic.storage_conditions_description,
            })
            
            # Get Drug Class
            if generic.drug_class_id:
                try:
                    drug_class = DrugClass.objects.get(id=generic.drug_class_id)
                    data['drug_class'] = drug_class.drug_class_name
                except DrugClass.DoesNotExist:
                    data['drug_class'] = generic.drug_class or 'N/A'
            else:
                data['drug_class'] = generic.drug_class or 'N/A'
            
            # Get Indication
            if generic.indication_id:
                try:
                    indication = Indication.objects.get(id=generic.indication_id)
                    data['indication'] = indication.indication_name
                except Indication.DoesNotExist:
                    data['indication'] = generic.indication or 'N/A'
            else:
                data['indication'] = generic.indication or 'N/A'
        else:
            # Default values if no generic
            data.update({
                'generic': 'N/A',
                'drug_class': 'N/A',
                'indication': 'N/A',
                'indication_desc': 'N/A',
                'pharmacology': 'N/A',
                'dosage': 'N/A',
                'administration': 'N/A',
                'interaction': 'N/A',
                'contraindications': 'N/A',
                'side_effects': 'N/A',
                'pregnancy': 'N/A',
                'precautions': 'N/A',
            })
        
        # Get Manufacturer
        if drug.mfg_id:
            try:
                manufacturer = Manufacturer.objects.get(id=drug.mfg_id)
                data['manufacturer'] = manufacturer.manufacturer_name
            except Manufacturer.DoesNotExist:
                data['manufacturer'] = 'N/A'
        else:
            data['manufacturer'] = 'N/A'
        
        # Get Dosage Form
        if drug.dosage_form_id:
            try:
                dosage_form = DosageForm.objects.get(id=drug.dosage_form_id)
                data['dosage_form'] = dosage_form.dosage_form_name
                data['dosage_form_short'] = dosage_form.short_name
            except DosageForm.DoesNotExist:
                data['dosage_form'] = 'N/A'
                data['dosage_form_short'] = 'N/A'
        else:
            data['dosage_form'] = 'N/A'
            data['dosage_form_short'] = 'N/A'
        
        return JsonResponse({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
