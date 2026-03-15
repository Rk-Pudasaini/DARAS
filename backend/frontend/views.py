from django.shortcuts import render

def use_model(request):
    # Use the correct path relative to the templates folder
    return render(request, 'pages/use_model.html')

def digital_usage(request):
    return render(request, 'pages/digital_usage.html')

def risk_category(request):
    return render(request, 'pages/risk_category.html')

def metrics(request):
    return render(request, 'pages/metrics.html')

def about(request):
    return render(request, 'pages/about.html')