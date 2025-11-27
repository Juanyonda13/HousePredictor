// Cargar estadísticas al iniciar
      window.addEventListener("load", function () {
        fetch("/api/estadisticas")
          .then((response) => response.json())
          .then((data) => {
            const statsHTML = `
                        <p class="mb-2"><strong>Total de casas:</strong> ${data.total_casas.toLocaleString()}</p>
                        <p class="mb-2"><strong>Precio promedio:</strong> $${data.precio_promedio.toLocaleString(
                          "en-US",
                          { maximumFractionDigits: 0 }
                        )}</p>
                        <p class="mb-2"><strong>Precio mínimo:</strong> $${data.precio_min.toLocaleString(
                          "en-US",
                          { maximumFractionDigits: 0 }
                        )}</p>
                        <p class="mb-2"><strong>Precio máximo:</strong> $${data.precio_max.toLocaleString(
                          "en-US",
                          { maximumFractionDigits: 0 }
                        )}</p>
                        <p class="mb-0"><strong>Mediana:</strong> $${data.precio_mediana.toLocaleString(
                          "en-US",
                          { maximumFractionDigits: 0 }
                        )}</p>
                    `;
            document.getElementById("statsContent").innerHTML = statsHTML;
          })
          .catch((error) => {
            document.getElementById("statsContent").innerHTML =
              '<p class="text-warning">No disponible</p>';
          });
      });

      // Manejar envío del formulario
      document
        .getElementById("predictionForm")
        .addEventListener("submit", function (e) {
          e.preventDefault();

          const formData = new FormData(this);
          const data = Object.fromEntries(formData.entries());

          // Mostrar loading
          const btn = this.querySelector('button[type="submit"]');
          const spinner = btn.querySelector(".loading-spinner");
          spinner.classList.add("show");
          btn.disabled = true;

          // Ocultar resultado anterior
          document.getElementById("resultCard").classList.remove("show");

          // Enviar predicción con paso a paso
          fetch("/api/predecir?paso_a_paso=true", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
          })
            .then((response) => response.json())
            .then((result) => {
              spinner.classList.remove("show");
              btn.disabled = false;

              if (result.error) {
                alert("Error: " + result.error);
              } else {
                // Formatear precio
                const precio = new Intl.NumberFormat("es-US", {
                  style: "currency",
                  currency: "USD",
                  minimumFractionDigits: 0,
                  maximumFractionDigits: 0,
                }).format(result.precio);

                document.getElementById("priceDisplay").textContent = precio;

                // Mostrar intervalo de confianza si existe
                if (result.ic_inferior && result.ic_superior) {
                  const icInf = new Intl.NumberFormat("es-US", {
                    style: "currency",
                    currency: "USD",
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0,
                  }).format(result.ic_inferior);

                  const icSup = new Intl.NumberFormat("es-US", {
                    style: "currency",
                    currency: "USD",
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0,
                  }).format(result.ic_superior);

                  document.getElementById(
                    "icRange"
                  ).textContent = `${icInf} - ${icSup}`;
                  document.getElementById("confidenceInterval").style.display =
                    "block";
                }

                // Mostrar R² si existe
                if (result.r2) {
                  document.getElementById("r2Value").textContent =
                    (result.r2 * 100).toFixed(2) + "%";
                  document.getElementById("r2Info").style.display = "block";
                }

                // Almacenar datos de ambos modelos para paso a paso
                window.modelosData = result.modelos || {};
                
                // DEBUG: Verificar qué datos llegaron
                console.log("🔍 Datos recibidos del servidor:", result);
                console.log("📦 window.modelosData:", window.modelosData);
                if (result.modelos) {
                  console.log("  - OLS disponible:", !!result.modelos.ols);
                  console.log("  - Paso a paso OLS:", result.modelos.ols?.paso_a_paso?.length || 0, "pasos");
                  console.log("  - Bayesiano disponible:", !!result.modelos.bayesiano);
                  console.log("  - Paso a paso Bayesiano:", result.modelos.bayesiano?.paso_a_paso?.length || 0, "pasos");
                }
                
                // Mostrar ambos modelos trabajando juntos
                if (result.modelos && result.modelos.ols && result.modelos.bayesiano) {
                  // Calcular precio promedio consensuado
                  const precioPromedio = (result.modelos.ols.precio + result.modelos.bayesiano.precio) / 2;
                  const precioConsensuado = new Intl.NumberFormat("es-US", {
                    style: "currency",
                    currency: "USD",
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0,
                  }).format(precioPromedio);
                  
                  // Actualizar precio principal con el consensuado
                  document.getElementById("priceDisplay").textContent = precioConsensuado;
                  
                  // Calcular intervalo combinado (rango más amplio para cubrir ambos)
                  const icMin = Math.min(result.modelos.ols.ic_inferior, result.modelos.bayesiano.ic_inferior);
                  const icMax = Math.max(result.modelos.ols.ic_superior, result.modelos.bayesiano.ic_superior);
                  
                  const icInf = new Intl.NumberFormat("es-US", {
                    style: "currency",
                    currency: "USD",
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0,
                  }).format(icMin);
                  
                  const icSup = new Intl.NumberFormat("es-US", {
                    style: "currency",
                    currency: "USD",
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0,
                  }).format(icMax);
                  
                  document.getElementById("icRange").textContent = `${icInf} - ${icSup}`;
                  document.getElementById("confidenceInterval").style.display = "block";
                  
                  // Mostrar que ambos modelos contribuyeron
                  const precioOLS = new Intl.NumberFormat("es-US", {
                    style: "currency",
                    currency: "USD",
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0,
                  }).format(result.modelos.ols.precio);
                  
                  const precioBayes = new Intl.NumberFormat("es-US", {
                    style: "currency",
                    currency: "USD",
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0,
                  }).format(result.modelos.bayesiano.precio);
                  
                  document.getElementById("precioOLS").textContent = precioOLS;
                  document.getElementById("precioBayes").textContent = precioBayes;
                  document.getElementById("modelosComparacion").style.display = "block";
                  
                  // Actualizar información del modelo para mostrar colaboración
                  document.getElementById("modelInfo").innerHTML = 
                    'Análisis integrado: OLS y Regresión Bayesiana';
                } else if (result.modelos && result.modelos.ols) {
                  document.getElementById("modelosComparacion").style.display = "none";
                  document.getElementById("modelInfo").textContent = "Regresión Lineal Múltiple (OLS)";
                } else if (result.modelos && result.modelos.bayesiano) {
                  document.getElementById("modelosComparacion").style.display = "none";
                  document.getElementById("modelInfo").textContent = "Regresión Bayesiana (Teorema de Bayes)";
                }
                
                // Determinar si hay paso a paso disponible
                let tienePasoAPaso = false;
                if (result.modelos) {
                  if (result.modelos.ols && result.modelos.ols.paso_a_paso) {
                    tienePasoAPaso = true;
                  }
                  if (result.modelos.bayesiano && result.modelos.bayesiano.paso_a_paso) {
                    tienePasoAPaso = true;
                  }
                }
                
                // Mostrar botón de fórmulas si existe paso a paso
                if (tienePasoAPaso) {
                  document.getElementById("btnVerFormulas").style.display =
                    "inline-block";
                }

                document.getElementById("resultCard").classList.add("show");
              }
            })
            .catch((error) => {
              spinner.classList.remove("show");
              btn.disabled = false;
              alert("Error en la predicción: " + error);
            });
        });

      // Cargar datos de ejemplo
      function cargarEjemplo() {
        fetch("/api/datos-ejemplo")
          .then((response) => response.json())
          .then((data) => {
            const form = document.getElementById("predictionForm");
            Object.keys(data).forEach((key) => {
              const input = form.querySelector(`[name="${key}"]`);
              if (input) {
                input.value = data[key];
              }
            });
          })
          .catch((error) => alert("Error al cargar ejemplo: " + error));
      }

      // Ver información del modelo
      function verModelo() {
        fetch("/api/modelo-info")
          .then((response) => response.json())
          .then((data) => {
            let info = "";
            
            if (data.modelos) {
              // Mostrar información de ambos modelos si están disponibles
              if (data.modelos.ols) {
                info += `\nMODELO OLS (Frecuentista):\n`;
                info += `Metodología: ${data.modelos.ols.metodologia}\n`;
                info += `Framework: ${data.modelos.ols.framework}\n`;
                info += `\nMétricas:\n`;
                info += `- R²: ${data.modelos.ols.metricas.r2.toFixed(4)} (${(data.modelos.ols.metricas.r2 * 100).toFixed(2)}%)\n`;
                info += `- R² Ajustado: ${data.modelos.ols.metricas.r2_ajustado.toFixed(4)}\n`;
                info += `- RMSE: $${data.modelos.ols.metricas.rmse.toLocaleString()}\n`;
                info += `- Observaciones: ${data.modelos.ols.metricas.n_observaciones}\n`;
                info += `- Variables: ${data.modelos.ols.metricas.n_variables}\n`;
              }
              
              if (data.modelos.bayesiano) {
                if (info) info += `\n${"=".repeat(40)}\n`;
                info += `\nMODELO BAYESIANO:\n`;
                info += `Metodología: ${data.modelos.bayesiano.metodologia}\n`;
                info += `Framework: ${data.modelos.bayesiano.framework}\n`;
                info += `Prior: ${data.modelos.bayesiano.prior || 'No informativo'}\n`;
                info += `\nMétricas:\n`;
                info += `- R²: ${data.modelos.bayesiano.metricas.r2.toFixed(4)} (${(data.modelos.bayesiano.metricas.r2 * 100).toFixed(2)}%)\n`;
                info += `- R² Ajustado: ${data.modelos.bayesiano.metricas.r2_ajustado.toFixed(4)}\n`;
                info += `- RMSE: $${data.modelos.bayesiano.metricas.rmse.toLocaleString()}\n`;
                info += `- Observaciones: ${data.modelos.bayesiano.metricas.n_observaciones}\n`;
                info += `- Variables: ${data.modelos.bayesiano.metricas.n_variables}\n`;
              }
              
              if (data.modelos.ols && data.modelos.bayesiano) {
                info += `\n${"=".repeat(40)}\n`;
                info += `\nAmbos modelos usan el Teorema de Bayes:\n`;
                info += `- OLS: Método frecuentista (coeficientes fijos)\n`;
                info += `- Bayesiano: Aplica P(β|datos) ∝ P(datos|β) × P(β)\n`;
              }
            } else {
              // Compatibilidad con formato anterior
              info = `
                        Tipo: ${data.tipo_modelo || 'No disponible'}
                        Framework: ${data.framework || 'No disponible'}
                        
                        Métricas:
                        - R²: ${data.metricas?.r2?.toFixed(4) || 'N/A'}
                        - R² Ajustado: ${data.metricas?.r2_ajustado?.toFixed(4) || 'N/A'}
                        - RMSE: $${data.metricas?.rmse?.toLocaleString() || 'N/A'}
                        - Observaciones: ${data.metricas?.n_observaciones || 'N/A'}
                    `;
            }
            
            alert(info || "Información no disponible");
          })
          .catch((error) => alert("Error al obtener info del modelo: " + error));
      }

      // Mostrar fórmulas y paso a paso
      function mostrarFormulas() {
        const formulasCard = document.getElementById("formulasCard");
        const formulasContent = document.getElementById("formulasContent");

        if (!window.modelosData || (!window.modelosData.ols && !window.modelosData.bayesiano)) {
          alert("No hay datos de paso a paso disponibles");
          return;
        }

        let html = "";
        
        // Mostrar análisis integrado si hay ambos modelos
        if (window.modelosData.ols && window.modelosData.bayesiano) {
          const precioPromedio = (window.modelosData.ols.precio + window.modelosData.bayesiano.precio) / 2;
          html += `<div class="step-card" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none;">`;
          html += `<h5><span class="step-number">0</span>Análisis Estadístico Integrado</h5>`;
          html += `<p class="text-white mb-3">El sistema procesa los datos simultáneamente con ambos métodos para obtener una predicción consensuada:</p>`;
          html += `<div class="mb-3 p-3" style="background: rgba(255,255,255,0.3); border-radius: 8px;">`;
          html += `<h6 class="mb-2">Precio Consensuado (Promedio)</h6>`;
          html += `<p class="mb-0" style="font-size: 1.2rem;"><strong>$${precioPromedio.toLocaleString()}</strong></p>`;
          html += `</div>`;
          html += `<div class="row mt-3">`;
          html += `<div class="col-md-6">`;
          html += `<div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px;">`;
          html += `<h6>Análisis OLS</h6>`;
          html += `<p class="mb-1"><strong>Precio:</strong> $${window.modelosData.ols.precio.toLocaleString()}</p>`;
          html += `<p class="mb-0"><strong>IC 95%:</strong> $${window.modelosData.ols.ic_inferior.toLocaleString()} - $${window.modelosData.ols.ic_superior.toLocaleString()}</p>`;
          html += `</div></div>`;
          html += `<div class="col-md-6">`;
          html += `<div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px;">`;
          html += `<h6>Análisis Bayesiano</h6>`;
          html += `<p class="mb-1"><strong>Precio:</strong> $${window.modelosData.bayesiano.precio.toLocaleString()}</p>`;
          html += `<p class="mb-0"><strong>IC 95%:</strong> $${window.modelosData.bayesiano.ic_inferior.toLocaleString()} - $${window.modelosData.bayesiano.ic_superior.toLocaleString()}</p>`;
          html += `</div></div>`;
          html += `</div>`;
          html += `<p class="text-white-50 mt-3 mb-0" style="font-size: 0.9rem;">Ambos modelos analizan los mismos datos usando diferentes metodologías estadísticas, proporcionando una predicción más robusta y confiable.</p>`;
          html += `</div>`;
        }

        // Mostrar paso a paso de OLS
        if (window.modelosData.ols && window.modelosData.ols.paso_a_paso) {
          html += `<div class="mt-4"><h4 class="mb-3" style="color: var(--primary-color);">Método OLS (Frecuentista)</h4></div>`;
          window.modelosData.ols.paso_a_paso.forEach((paso, index) => {
          html += `<div class="step-card">`;
          html += `<h5><span class="step-number">${index + 1}</span>${paso.titulo}</h5>`;

          if (paso.descripcion) {
            html += `<p class="text-muted">${paso.descripcion}</p>`;
          }

          if (paso.formula) {
            html += `<div class="formula-box">`;
            html += `<div class="formula">${paso.formula}</div>`;
            if (paso.formula_general) {
              html += `<div class="formula descripcion mt-2">${paso.formula_general}</div>`;
            }
              if (paso.interpretacion) {
              html += `<div class="descripcion"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
            }
            html += `</div>`;
          }

          // Variables preparadas
          if (paso.variables) {
            html += `<div class="mt-3">`;
            html += `<strong>Variables:</strong>`;
            Object.keys(paso.variables).forEach((key) => {
              html += `<div class="variable-item">`;
              html += `<strong>${key}:</strong> ${paso.variables[key]}`;
              // Mostrar tipo de variable aleatoria si está disponible
              if (paso.tipos_variables && paso.tipos_variables[key]) {
                html += `<br><small class="text-muted" style="font-style: italic;">📊 Tipo: ${paso.tipos_variables[key]}</small>`;
              }
              html += `</div>`;
            });
            html += `</div>`;
          }

          // Coeficientes
          if (paso.coeficientes) {
            html += `<div class="mt-3">`;
            html += `<strong>Coeficientes (β):</strong>`;
            Object.keys(paso.coeficientes).forEach((key) => {
              const coef = paso.coeficientes[key];
              html += `<div class="coeficiente-item">`;
              html += `<div><strong>${key}:</strong> <span class="valor">${coef.valor.toFixed(2)}</span></div>`;
              if (coef.p_valor !== null) {
                const significativo = coef.significativo;
                html += `<div class="p-valor">`;
                html += `p-valor: ${coef.p_valor.toFixed(4)} `;
                html += `<span class="${significativo ? "significativo" : "no-significativo"}">(${significativo ? "Significativo" : "No significativo"})</span>`;
                html += `</div>`;
              }
              html += `</div>`;
            });
            html += `</div>`;
          }

          // Términos del cálculo
          if (paso.terminos) {
            html += `<div class="mt-3">`;
            html += `<strong>Cálculo de Términos:</strong>`;
            paso.terminos.forEach((termino) => {
              html += `<div class="termino-item">`;
              html += `<div>`;
              html += `<strong>${termino.variable}:</strong> `;
              html += `β = ${termino.coeficiente.toFixed(2)}, `;
              html += `X = ${termino.valor}`;
              html += `</div>`;
              html += `<div class="valor">${termino.formula}</div>`;
              html += `</div>`;
            });
            html += `</div>`;
          }

          // Constante y suma
          if (paso.constante !== undefined) {
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">Constante (β₀): ${paso.constante.toFixed(2)}</div>`;
            html += `<div class="formula">Suma de términos: ${paso.suma_terminos.toFixed(2)}</div>`;
            html += `<div class="formula">${paso.formula}</div>`;
            html += `</div>`;
          }

          // Intervalo de confianza
          if (paso.ic_inferior !== undefined) {
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">${paso.formula}</div>`;
            if (paso.margen_error) {
              html += `<div class="descripcion">Margen de error: $${paso.margen_error.toLocaleString()}</div>`;
            }
                if (paso.interpretacion) {
                html += `<div class="descripcion mt-2"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
              }
            html += `</div>`;
          }

          // Métricas
          if (paso.r2 !== undefined) {
            html += `<div class="formula-box mt-3">`;
            html += `<div class="formula">R² = ${paso.r2.toFixed(4)} (${(paso.r2 * 100).toFixed(2)}%)</div>`;
            if (paso.r2_ajustado) {
              html += `<div class="formula">R² Ajustado = ${paso.r2_ajustado.toFixed(4)}</div>`;
            }
            if (paso.rmse) {
              html += `<div class="formula">RMSE = $${paso.rmse.toLocaleString()}</div>`;
            }
            if (paso.formula_r2) {
              html += `<div class="descripcion">${paso.formula_r2}</div>`;
            }
                if (paso.interpretacion) {
                html += `<div class="descripcion mt-2"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
              }
            html += `</div>`;
          }

          html += `</div>`;
          });
        }

        // Mostrar paso a paso Bayesiano
        console.log("🔍 Verificando datos bayesianos:", window.modelosData.bayesiano);
        if (window.modelosData.bayesiano && window.modelosData.bayesiano.paso_a_paso) {
          console.log("✅ Datos bayesianos encontrados, pasos:", window.modelosData.bayesiano.paso_a_paso.length);
          html += `<div class="mt-5"><h4 class="mb-3" style="color: var(--secondary-color);">Método Bayesiano (Teorema de Bayes)</h4></div>`;
          window.modelosData.bayesiano.paso_a_paso.forEach((paso, index) => {
            console.log(`  Procesando paso ${index + 1}: ${paso.titulo}`);
            html += `<div class="step-card">`;
            html += `<h5><span class="step-number">${index + 1}</span>${paso.titulo}</h5>`;

            if (paso.descripcion) {
              html += `<p class="text-muted">${paso.descripcion}</p>`;
            }

            if (paso.formula) {
              html += `<div class="formula-box">`;
              html += `<div class="formula">${paso.formula}</div>`;
              if (paso.formula_desarrollada) {
                html += `<div class="formula descripcion mt-2">${paso.formula_desarrollada}</div>`;
              }
              if (paso.formula_general) {
                html += `<div class="formula descripcion mt-2">${paso.formula_general}</div>`;
              }
              if (paso.formula_nombres) {
                html += `<div class="descripcion mt-2"><strong>${paso.formula_nombres}</strong></div>`;
              }
                if (paso.interpretacion) {
                html += `<div class="descripcion mt-2"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
              }
              html += `</div>`;
            }

            // Prior (Paso 1)
            if (paso.prior_tipo) {
              html += `<div class="formula-box mt-3">`;
              html += `<div class="formula">${paso.prior_formula || paso.formula}</div>`;
              html += `<div class="descripcion">Tipo: ${paso.prior_tipo}</div>`;
                if (paso.interpretacion) {
                html += `<div class="descripcion mt-2"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
              }
              html += `</div>`;
            }

            // Verosimilitud (Paso 2)
            if (paso.formula_estimacion || (paso.titulo && paso.titulo.includes('Verosimilitud'))) {
              html += `<div class="formula-box mt-3">`;
              if (paso.formula) {
                html += `<div class="formula">${paso.formula}</div>`;
              }
              if (paso.formula_desarrollada) {
                html += `<div class="formula descripcion mt-2">${paso.formula_desarrollada}</div>`;
              }
              if (paso.formula_estimacion) {
                html += `<div class="formula descripcion mt-2">${paso.formula_estimacion}</div>`;
              }
                if (paso.interpretacion) {
                html += `<div class="descripcion mt-2"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
              }
              html += `</div>`;
            }

            // Posterior (Paso 3)
            if (paso.posterior_tipo) {
              html += `<div class="formula-box mt-3">`;
              html += `<div class="formula">${paso.formula}</div>`;
              if (paso.formula_desarrollada) {
                html += `<div class="formula descripcion mt-2">${paso.formula_desarrollada}</div>`;
              }
              html += `<div class="descripcion">Tipo: ${paso.posterior_tipo}</div>`;
                if (paso.interpretacion) {
                html += `<div class="descripcion mt-2"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
              }
              html += `</div>`;
            }

            // Beta media posterior (si está en el paso de posterior)
            if (paso.beta_media && typeof paso.beta_media === 'object') {
              html += `<div class="mt-3"><strong>Media Posterior (E[β|datos]):</strong>`;
              Object.keys(paso.beta_media).forEach((key) => {
                const valor = paso.beta_media[key];
                html += `<div class="variable-item">`;
                html += `<strong>${key}:</strong> ${typeof valor === 'number' ? valor.toFixed(2) : valor}`;
                html += `</div>`;
              });
              html += `</div>`;
            }

            // Variables (Paso 4)
            if (paso.variables) {
              html += `<div class="mt-3"><strong>Variables:</strong>`;
              Object.keys(paso.variables).forEach((key) => {
                html += `<div class="variable-item">`;
                html += `<strong>${key}:</strong> ${paso.variables[key]}`;
                // Mostrar tipo de variable aleatoria si está disponible
                if (paso.tipos_variables && paso.tipos_variables[key]) {
                  html += `<br><small class="text-muted" style="font-style: italic;">📊 Tipo: ${paso.tipos_variables[key]}</small>`;
                }
                html += `</div>`;
              });
              html += `</div>`;
            }

            // Coeficientes bayesianos
            if (paso.coeficientes) {
              html += `<div class="mt-3"><strong>Coeficientes Posteriores:</strong>`;
              Object.keys(paso.coeficientes).forEach((key) => {
                const coef = paso.coeficientes[key];
                html += `<div class="coeficiente-item">`;
                html += `<div><strong>${key}:</strong> <span class="valor">${coef.valor.toFixed(2)}</span></div>`;
                if (coef.desviacion_estandar !== undefined) {
                  html += `<div class="p-valor">Desv. Est.: ±${coef.desviacion_estandar.toFixed(2)}</div>`;
                }
                if (coef.interpretacion) {
                  html += `<div class="descripcion">${coef.interpretacion}</div>`;
                }
                html += `</div>`;
              });
              html += `</div>`;
            }

            // Términos del cálculo bayesiano (similar a OLS)
            if (paso.terminos) {
              html += `<div class="mt-3"><strong>Cálculo de Términos:</strong>`;
              paso.terminos.forEach((termino) => {
                html += `<div class="termino-item">`;
                html += `<div><strong>${termino.variable}:</strong> β = ${termino.coeficiente.toFixed(2)}, X = ${termino.valor}</div>`;
                html += `<div class="valor">${termino.formula}</div>`;
                html += `</div>`;
              });
              html += `</div>`;
            }

            // Constante y suma (Paso 6)
            if (paso.constante !== undefined && paso.suma_terminos !== undefined) {
              html += `<div class="formula-box mt-3">`;
              html += `<div class="formula">Constante (β₀): ${paso.constante.toFixed(2)}</div>`;
              html += `<div class="formula">Suma de términos: ${paso.suma_terminos.toFixed(2)}</div>`;
              if (paso.formula_desarrollada) {
                html += `<div class="formula">${paso.formula_desarrollada}</div>`;
              }
              if (paso.formula) {
                html += `<div class="formula descripcion mt-2">${paso.formula}</div>`;
              }
                if (paso.interpretacion) {
                html += `<div class="descripcion mt-2"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
              }
              html += `</div>`;
            }

            // Distribución predictiva posterior (Paso 7)
            if (paso.varianza_prediccion !== undefined) {
              html += `<div class="formula-box mt-3">`;
              html += `<div class="formula">${paso.formula || 'Distribución Predictiva Posterior'}</div>`;
              if (paso.formula_desarrollada) {
                html += `<div class="formula descripcion mt-2">${paso.formula_desarrollada}</div>`;
              }
              html += `<div class="descripcion mt-2">Varianza: ${paso.varianza_prediccion.toFixed(2)}</div>`;
              html += `<div class="descripcion">Desviación estándar: ${paso.desviacion_estandar.toFixed(2)}</div>`;
                if (paso.interpretacion) {
                html += `<div class="descripcion mt-2"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
              }
              html += `</div>`;
            }

            // Comparación OLS vs Bayesiano
            if (paso.comparacion) {
              html += `<div class="formula-box mt-3">`;
              html += `<div class="formula">Comparación de Enfoques</div>`;
              html += `<div class="row mt-3">`;
              html += `<div class="col-md-6"><strong>Frecuentista (OLS):</strong><ul>`;
              Object.keys(paso.comparacion.frecuentista).forEach((key) => {
                html += `<li><strong>${key}:</strong> ${paso.comparacion.frecuentista[key]}</li>`;
              });
              html += `</ul></div>`;
              html += `<div class="col-md-6"><strong>Bayesiano:</strong><ul>`;
              Object.keys(paso.comparacion.bayesiano).forEach((key) => {
                html += `<li><strong>${key}:</strong> ${paso.comparacion.bayesiano[key]}</li>`;
              });
              html += `</ul></div>`;
              html += `</div>`;
                if (paso.ventaja_bayesiana) {
                html += `<div class="descripcion mt-2"><strong>Nota:</strong> ${paso.ventaja_bayesiana}</div>`;
              }
              html += `</div>`;
            }

            // Intervalo creíble (Paso 8)
            if (paso.ic_inferior !== undefined) {
              html += `<div class="formula-box mt-3">`;
              html += `<div class="formula">${paso.formula}</div>`;
              if (paso.formula_general) {
                html += `<div class="formula descripcion mt-2">${paso.formula_general}</div>`;
              }
              if (paso.margen_error !== undefined) {
                html += `<div class="descripcion">Margen de error: $${paso.margen_error.toLocaleString()}</div>`;
              }
                if (paso.interpretacion) {
                html += `<div class="descripcion mt-2"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
              }
              if (paso.diferencia_ols) {
                html += `<div class="descripcion mt-2" style="background: #fff3cd; padding: 0.5rem; border-radius: 5px; border-left: 3px solid #ffc107;"><strong>Nota:</strong> ${paso.diferencia_ols}</div>`;
              }
              html += `</div>`;
            }

            // Métricas del modelo bayesiano (si están en un paso separado)
            if (paso.r2 !== undefined && !paso.varianza_prediccion) {
              html += `<div class="formula-box mt-3">`;
              html += `<div class="formula">R² = ${paso.r2.toFixed(4)} (${(paso.r2 * 100).toFixed(2)}%)</div>`;
              if (paso.r2_ajustado) {
                html += `<div class="formula">R² Ajustado = ${paso.r2_ajustado.toFixed(4)}</div>`;
              }
              if (paso.rmse) {
                html += `<div class="formula">RMSE = $${paso.rmse.toLocaleString()}</div>`;
              }
              if (paso.formula_r2) {
                html += `<div class="descripcion">${paso.formula_r2}</div>`;
              }
                if (paso.interpretacion) {
                html += `<div class="descripcion mt-2"><strong>Nota:</strong> ${paso.interpretacion}</div>`;
              }
              html += `</div>`;
            }

            html += `</div>`;
          });
        }

        // Debug: verificar qué se va a mostrar
        console.log("📊 Total de HTML generado:", html.length, "caracteres");
        console.log("📋 Resumen de contenido:");
        console.log("  - OLS:", window.modelosData.ols ? "✅ Disponible" : "❌ No disponible");
        console.log("  - Bayesiano:", window.modelosData.bayesiano ? "✅ Disponible" : "❌ No disponible");
        if (window.modelosData.bayesiano) {
          console.log("  - Paso a paso bayesiano:", window.modelosData.bayesiano.paso_a_paso ? "✅ Disponible (" + window.modelosData.bayesiano.paso_a_paso.length + " pasos)" : "❌ No disponible");
        }
        
        if (!window.modelosData.bayesiano || !window.modelosData.bayesiano.paso_a_paso) {
          html += `<div class="alert alert-warning mt-4" style="background: #fff3cd; border: 1px solid #ffc107; padding: 1rem; border-radius: 8px;">`;
          html += `<strong>Paso a paso Bayesiano no disponible</strong><br>`;
          html += `<small>El modelo bayesiano no está cargado o no se generó el paso a paso. Verifica que el modelo esté entrenado.</small>`;
          html += `</div>`;
        }

        formulasContent.innerHTML = html;
        formulasCard.classList.add("show");
        formulasCard.scrollIntoView({ behavior: "smooth", block: "start" });
      }
