let isDirty = false;

let pendingParams =
    new URLSearchParams(window.location.search);


// =====================================================
// ACTION BUTTONS
// =====================================================

function markDirty() {

    const current =
        new URLSearchParams(
            window.location.search
        ).toString();

    const pending =
        pendingParams.toString();

    isDirty = current !== pending;

    updateActionButtons();
}

function updateActionButtons() {

    const applyBtn =
        document.getElementById('apply-btn');

    const clearAllBtn =
        document.getElementById('clear-all-btn');

    const paramsForFilter =

        new URLSearchParams(

            pendingParams

        );

    paramsForFilter.delete(

        "status"

    );
    paramsForFilter.delete(

        "page"

    );

    const hasFilters =
        paramsForFilter.toString().length > 0;

    // APPLY

    if (isDirty) {

        applyBtn.disabled = false;

        applyBtn.classList.add('active');
        applyBtn.classList.remove('disabled');

    } else {

        applyBtn.disabled = true;

        applyBtn.classList.remove('active');
        applyBtn.classList.add('disabled');
    }

    // CLEAR ALL

    if (hasFilters) {

        clearAllBtn.classList.remove('hidden');

        clearAllBtn.disabled = false;

        clearAllBtn.classList.add('active');
        clearAllBtn.classList.remove('disabled');

    } else {

        clearAllBtn.classList.add('hidden');

        clearAllBtn.disabled = true;

        clearAllBtn.classList.remove('active');
        clearAllBtn.classList.add('disabled');
    }
}

function applyFilters() {

    window.location.search =
        pendingParams.toString();
}

function clearAllFilters() {

    pendingParams =
        new URLSearchParams();

    refreshAllFilterUI();
    evaluateDirtyState();
}

function evaluateDirtyState() {

    const current =
        new URLSearchParams(
            window.location.search
        ).toString();

    const pending =
        pendingParams.toString();

    isDirty = current !== pending;

    updateActionButtons();
}



// =====================================================
// YEAR FILTER
// =====================================================

document.querySelectorAll('.year-btn')
    .forEach(btn => {

        btn.addEventListener('click', () => {

            const year =
                btn.dataset.year;

            let selectedYears =
                new Set(
                    pendingParams.getAll('years')
                );

            if (selectedYears.has(year)) {

                selectedYears.delete(year);

            } else {

                selectedYears.add(year);
            }

            pendingParams.delete('years');

            selectedYears.forEach(y => {

                pendingParams.append(
                    'years',
                    y
                );

            });

            markDirty();

            refreshYearUI();

        });

    });

function refreshYearUI() {

    const selectedYears =
        new Set(
            pendingParams.getAll('years')
        );

    const card =
        document.querySelectorAll('.filter-card')[0];

    const clearBtn =
        card.querySelector('.clear-btn');

    // ACTIVE BUTTONS

    document.querySelectorAll('.year-btn')
        .forEach(btn => {

            const year =
                btn.dataset.year;

            if (selectedYears.has(year)) {

                btn.classList.add('active');

            } else {

                btn.classList.remove('active');
            }
        });

    // CARD ACTIVE

    if (selectedYears.size > 0) {

        card.classList.add('active');

        clearBtn.classList.remove('hidden');

    } else {

        card.classList.remove('active');

        clearBtn.classList.add('hidden');
    }
}

function clearYears() {

    pendingParams.delete('years');

    markDirty();

    refreshYearUI();
}



// =====================================================
// FIELD FILTER
// =====================================================

document.querySelectorAll('.field-btn')
    .forEach(btn => {

        btn.addEventListener('click', () => {

            const field =
                btn.dataset.field;

            let selectedFields =
                new Set(
                    pendingParams.getAll('fields')
                );

            if (selectedFields.has(field)) {

                selectedFields.delete(field);

            } else {

                selectedFields.add(field);
            }

            pendingParams.delete('fields');

            selectedFields.forEach(f => {

                pendingParams.append(
                    'fields',
                    f
                );

            });

            markDirty();

            refreshFieldUI();

        });

    });

function refreshFieldUI() {

    const selectedFields =
        new Set(
            pendingParams.getAll('fields')
        );

    const card =
        document.querySelectorAll('.filter-card')[1];

    const clearBtn =
        card.querySelector('.clear-btn');

    document.querySelectorAll('.field-btn')
        .forEach(btn => {

            const field =
                btn.dataset.field;

            if (selectedFields.has(field)) {

                btn.classList.add('active');

            } else {

                btn.classList.remove('active');
            }
        });

    if (selectedFields.size > 0) {

        card.classList.add('active');

        clearBtn.classList.remove('hidden');

    } else {

        card.classList.remove('active');

        clearBtn.classList.add('hidden');
    }
}

function clearFields() {

    pendingParams.delete('fields');

    markDirty();

    refreshFieldUI();
}



// =====================================================
// ROLE FILTER
// =====================================================

document
    .getElementById('first-checkbox')
    .addEventListener('change', function (e) {

        if (e.target.checked) {

            pendingParams.set(
                'first',
                'true'
            );

        } else {

            pendingParams.delete('first');
        }

        markDirty();

        refreshRoleUI();
    });

document
    .getElementById('corresponding-checkbox')
    .addEventListener('change', function (e) {

        if (e.target.checked) {

            pendingParams.set(
                'corresponding',
                'true'
            );

        } else {

            pendingParams.delete(
                'corresponding'
            );
        }

        markDirty();

        refreshRoleUI();
    });

function refreshRoleUI() {

    const card =
        document.querySelectorAll('.filter-card')[2];

    const clearBtn =
        card.querySelector('.clear-btn');

    const first =
        pendingParams.get('first');

    const corresponding =
        pendingParams.get(
            'corresponding'
        );

    document.getElementById(
        'first-checkbox'
    ).checked = !!first;

    document.getElementById(
        'corresponding-checkbox'
    ).checked = !!corresponding;

    if (first || corresponding) {

        card.classList.add('active');

        clearBtn.classList.remove('hidden');

    } else {

        card.classList.remove('active');

        clearBtn.classList.add('hidden');
    }
}

function clearRoles() {

    pendingParams.delete('first');

    pendingParams.delete('corresponding');

    markDirty();

    refreshRoleUI();
}



// =====================================================
// CITATION FILTER
// =====================================================

document.querySelectorAll('.citation-checkbox')
    .forEach(cb => {

        cb.addEventListener('change', () => {

            updateCitationQuery();

        });

    });

function updateCitationQuery() {

    pendingParams.delete('citations');

    document.querySelectorAll(
        '.citation-checkbox:checked'
    )
        .forEach(cb => {

            pendingParams.append(
                'citations',
                cb.value
            );

        });

    markDirty();

    refreshCitationUI();
}

function refreshCitationUI() {

    const selected =
        new Set(
            pendingParams.getAll(
                'citations'
            )
        );

    const card =
        document.querySelectorAll('.filter-card')[3];

    const clearBtn =
        card.querySelector('.clear-btn');

    document.querySelectorAll(
        '.citation-checkbox'
    )
        .forEach(cb => {

            cb.checked =
                selected.has(cb.value);
        });

    if (selected.size > 0) {

        card.classList.add('active');

        clearBtn.classList.remove('hidden');

    } else {

        card.classList.remove('active');

        clearBtn.classList.add('hidden');
    }
}

function clearCitations() {

    pendingParams.delete('citations');

    markDirty();

    refreshCitationUI();
}



// =====================================================
// GLOBAL
// =====================================================

function refreshAllFilterUI() {

    refreshYearUI();

    refreshFieldUI();

    refreshRoleUI();

    refreshCitationUI();
}

document.addEventListener(
    'DOMContentLoaded',
    () => {

        refreshAllFilterUI();

        updateActionButtons();

    }
);