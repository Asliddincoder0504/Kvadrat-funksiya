import io
import base64
import math
import numpy as np
import matplotlib.pyplot as plt
from django.shortcuts import render
from .forms import QuadraticForm
from .models import EquationSolution


def generate_plot(a, b, c, x1=None, x2=None):
    if a == 0:
        return ""

    vertex_x = -b / (2 * a)


    base_range = 4.0
    if x1 is not None and x2 is not None:
        root_range = abs(x1 - x2) / 2 + 2
        x_range = max(base_range, root_range)
    else:
        x_range = base_range + abs(vertex_x) * 0.5

    x = np.linspace(vertex_x - x_range, vertex_x + x_range, 500)
    y = a * x**2 + b * x + c

    fig = plt.figure(figsize=(9, 6), facecolor='#1e1e2e', dpi=160)
    ax = fig.add_subplot(111, facecolor='#1e1e2e')

    ax.plot(x, y, color='#00d4ff', lw=2.5, label=f'f(x) = {a:g}x² {b:+g}x {c:+g}')

    ax.axhline(0, color='white', lw=0.8, alpha=0.7)
    ax.axvline(0, color='white', lw=0.8, alpha=0.7)

    if x1 is not None:
        ax.scatter([x1], [0], color='#ff4b5c', s=90, zorder=10, edgecolor='white', linewidth=1.2)
        ax.text(x1 + 0.2, 0.6 * max(y.min(), -1), f'x₁ = {x1:g}', color='#ff4b5c', fontsize=10)
    if x2 is not None and abs(x2 - x1) > 0.01:
        ax.scatter([x2], [0], color='#ff4b5c', s=90, zorder=10, edgecolor='white', linewidth=1.2)
        ax.text(x2 + 0.2, 0.6 * max(y.min(), -1), f'x₂ = {x2:g}', color='#ff4b5c', fontsize=10)

    # y o'qi chegarasini yanada ixcham qilish
    y_min, y_max = min(y), max(y)
    y_span = y_max - y_min if y_max != y_min else 10
    margin = y_span * 0.15
    ax.set_ylim(y_min - margin - 1, y_max + margin + 1)

    ax.grid(True, linestyle=':', alpha=0.4, color='white')
    ax.tick_params(colors='white', labelsize=9)
    ax.legend(fontsize=10, loc='upper right', framealpha=0.3)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=160, facecolor=fig.get_facecolor())
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return f"data:image/png;base64,{img_str}"



def home(request):
    form = QuadraticForm()
    step_by_step = ""
    graph = ""
    error = ""
    saved_id = None

    if request.method == "POST":
        form = QuadraticForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            c = form.cleaned_data['c']

            if abs(a) < 1e-10:
                error = "a koeffitsienti nolga yaqin — bu kvadrat tenglama emas!"
            else:
                D_raw = b ** 2 - 4 * a * c
                D = round(D_raw, 10)

                steps_list = [
                    f"1. Diskriminant: D = b² - 4ac = {b**2:g} - 4·{a:g}·{c:g} = {D:g}"
                ]

                roots_text = ""
                x1_val = x2_val = None

                if D > 1e-8:
                    x1_val = (-b + math.sqrt(D)) / (2 * a)
                    x2_val = (-b - math.sqrt(D)) / (2 * a)
                    roots_text = f"x₁ = {x1_val:g},   x₂ = {x2_val:g}"
                    steps_list.append(f"2. Ikkita haqiqiy ildiz: {roots_text}")
                elif abs(D) <= 1e-8:
                    x1_val = -b / (2 * a)
                    roots_text = f"x = {x1_val:g}"
                    steps_list.append(f"2. Bitta haqiqiy ildiz (takrorlanuvchi): {roots_text}")
                else:
                    real = -b / (2 * a)
                    imag = math.sqrt(-D) / (2 * a)
                    roots_text = f"{real:g} ± {imag:g}i"
                    steps_list.append(f"2. Kompleks ildizlar: {roots_text}")

                step_by_step = "<h4>Yechish bosqichlari:</h4>" + "<br>".join(steps_list)

                graph = generate_plot(a, b, c, x1_val, x2_val)

                solution = EquationSolution.objects.create(
                    a=a, b=b, c=c,
                    discriminant=D,
                    roots=roots_text,
                    steps="\n".join(steps_list)
                )
                saved_id = solution.id

    return render(request, 'solver/home.html', {
        'form': form,
        'step_by_step': step_by_step,
        'graph': graph,
        'error': error,
        'saved_id': saved_id,
    })


def history(request):
    solutions = EquationSolution.objects.all().order_by('-created_at')[:30]
    return render(request, 'solver/history.html', {'solutions': solutions})