(() => {
  // apps/site/lib/quickPlanner.ts
  var TARGET_WORK = [
    { value: "support", label: "IT support", hint: "Help desk, desktop, service desk" },
    { value: "networking", label: "Networking", hint: "Routing, switching, infrastructure" },
    { value: "security", label: "Cybersecurity", hint: "SOC, analysis, security operations" },
    { value: "cloud", label: "Cloud", hint: "AWS, Azure, or cloud operations" },
    { value: "unsure", label: "I am not sure yet", hint: "Choose the work before an exam" }
  ];
  var EXPERIENCE_STAGES = [
    { value: "new", label: "New to IT", hint: "No related job experience yet" },
    { value: "foundation", label: "Building a foundation", hint: "Studying or working in entry-level IT" },
    { value: "hands_on", label: "Doing the work", hint: "Regular hands-on responsibility in this area" },
    { value: "experienced", label: "Experienced", hint: "Own, lead, or design work in this area" }
  ];
  var PRIORITIES = [
    { value: "lowest_cost", label: "Lowest total cost", hint: "Avoid a cheap exam with expensive upkeep" },
    { value: "fastest_start", label: "Fastest honest start", hint: "The smallest credible next step" },
    { value: "strongest_role_fit", label: "Strongest role fit", hint: "Fit matters more than speed or price" }
  ];
  var CHECKED = "2026-08-09";
  var ROUTES = {
    aPlus: "/certifications/comptia/comptia-a-plus/",
    networkPlus: "/certifications/comptia/comptia-network-plus/",
    ccna: "/certifications/cisco/cisco-ccna/",
    isc2Cc: "/certifications/isc2/isc2-cc-certified-in-cybersecurity/",
    securityPlus: "/certifications/comptia/comptia-security-plus/",
    sscp: "/certifications/isc2/isc2-sscp-systems-security-certified-practitioner/",
    cism: "/certifications/isaca/isaca-cism-certified-information-security-manager/",
    cissp: "/certifications/isc2/isc2-cissp-certified-information-systems-security-professional/",
    awsCloudPractitioner: "/certifications/aws/aws-certified-cloud-practitioner/",
    az900: "/certifications/microsoft/microsoft-az-900/",
    awsSaa: "/certifications/aws/aws-solutions-architect-associate/",
    az104: "/certifications/microsoft/microsoft-az-104/",
    networkChoice: "/compare/comptia-network-plus-vs-cisco-ccna/",
    securityEntryChoice: "/compare/comptia-security-plus-vs-isc2-cc/",
    securityFoundationChoice: "/compare/isc2-sscp-vs-comptia-security-plus/",
    securityExperiencedChoice: "/compare/isaca-cism-vs-isc2-cissp/",
    cloudEntryChoice: "/compare/aws-cloud-practitioner-vs-microsoft-azure-fundamentals/",
    cloudHandsOnChoice: "/compare/microsoft-azure-administrator-vs-aws-solutions-architect-associate/"
  };
  var DECISIONS = {
    support: {
      new: {
        title: "Start with the A+ decision",
        route: ROUTES.aPlus,
        reason: "A+ is the reviewed public support credential RoleMath can currently stand behind for broad device, operating-system, and troubleshooting foundations.",
        nonFit: "Skip A+ if you already resolve support incidents independently or need an administration, networking, cloud, or security credential instead. RoleMath does not yet have complete public coverage of the other entry-support options.",
        credentialRoutes: [ROUTES.aPlus],
        primaryCredentialRoute: ROUTES.aPlus
      },
      foundation: {
        title: "Use A+ as a scope check",
        route: ROUTES.aPlus,
        reason: "At the foundation stage, A+ is useful only if its troubleshooting and support scope still fills a real gap in your work.",
        nonFit: "Do not buy A+ merely to collect another entry credential if your work has already moved into administration or infrastructure ownership. RoleMath does not yet have complete public coverage of the other entry-support options.",
        credentialRoutes: [ROUTES.aPlus],
        primaryCredentialRoute: ROUTES.aPlus
      },
      hands_on: null,
      experienced: null
    },
    networking: {
      new: {
        title: "Decide between Network+ and CCNA",
        route: ROUTES.networkChoice,
        reason: "The useful first decision is vendor-neutral networking foundation versus a more Cisco-specific, configuration-heavy route.",
        nonFit: "CCNA is not the fast option when routing and switching are still unfamiliar; Network+ is not the stronger next step when you already configure Cisco networks.",
        credentialRoutes: [ROUTES.networkPlus, ROUTES.ccna]
      },
      foundation: {
        title: "Decide between Network+ and CCNA",
        route: ROUTES.networkChoice,
        reason: "At the foundation stage, the right choice depends on whether you need broad concepts first or are ready to work directly in Cisco-oriented networking.",
        nonFit: "Skip Network+ if its objectives already describe work you can perform; skip CCNA for now if hands-on configuration is still the missing layer.",
        credentialRoutes: [ROUTES.networkPlus, ROUTES.ccna]
      },
      hands_on: {
        title: "Start with the CCNA decision",
        route: ROUTES.ccna,
        reason: "Regular hands-on networking makes CCNA the more decision-useful public option in RoleMath\u2019s current networking coverage.",
        nonFit: "Do not treat CCNA as proof of advanced design or architecture, and do not book it if the Cisco exam domains are not the work you want to practice.",
        credentialRoutes: [ROUTES.ccna],
        primaryCredentialRoute: ROUTES.ccna,
        alternative: {
          title: "Network+",
          route: ROUTES.networkPlus,
          when: "Use Network+ instead when you still need a vendor-neutral networking foundation before configuration depth.",
          credentialRoutes: [ROUTES.networkPlus]
        }
      },
      experienced: {
        title: "Use CCNA as a scope check, not an automatic next step",
        route: ROUTES.ccna,
        reason: "CCNA is the strongest current public networking leaf RoleMath can stand behind, but experienced practitioners should judge whether its scope is already below their work.",
        nonFit: "If you already design or lead networks, RoleMath does not yet have enough reviewed advanced-networking coverage to recommend your next credential.",
        credentialRoutes: [ROUTES.ccna],
        primaryCredentialRoute: ROUTES.ccna
      }
    },
    security: {
      new: {
        title: "Compare ISC2 CC with Security+",
        route: ROUTES.securityEntryChoice,
        reason: "The entry decision is whether you need a smaller cybersecurity starting point or the broader Security+ foundation.",
        nonFit: "Neither credential substitutes for basic IT and networking practice, and neither guarantees a security role.",
        credentialRoutes: [ROUTES.isc2Cc, ROUTES.securityPlus]
      },
      foundation: {
        title: "Start with the Security+ decision",
        route: ROUTES.securityPlus,
        reason: "Security+ is the clearest current public foundation anchor once you have basic IT context and want broader security coverage.",
        nonFit: "Do not use Security+ as a substitute for hands-on networking, systems, or lab practice, and skip it if its scope is already below your daily work.",
        credentialRoutes: [ROUTES.securityPlus],
        primaryCredentialRoute: ROUTES.securityPlus,
        alternative: {
          title: "ISC2 CC",
          route: ROUTES.isc2Cc,
          when: "Use ISC2 CC as the smaller first step when Security+ is still too broad for your current foundation.",
          credentialRoutes: [ROUTES.isc2Cc]
        }
      },
      hands_on: {
        title: "Compare SSCP with Security+",
        route: ROUTES.securityFoundationChoice,
        reason: "Hands-on security work makes the experience and certification boundary between SSCP and Security+ more important than a generic entry ranking.",
        nonFit: "SSCP has an experience gate; passing its exam is not the same as immediately holding the certification when that gate is unmet.",
        credentialRoutes: [ROUTES.sscp, ROUTES.securityPlus]
      },
      experienced: {
        title: "Decide between CISM and CISSP by job scope",
        route: ROUTES.securityExperiencedChoice,
        reason: "For experienced practitioners, management responsibility versus broad security-practice scope is a more useful boundary than exam price or speed.",
        nonFit: "Both credentials carry meaningful experience requirements; neither is an entry credential or a substitute for checking the exact eligibility terms.",
        credentialRoutes: [ROUTES.cism, ROUTES.cissp]
      }
    },
    cloud: {
      new: {
        title: "Choose a cloud platform before an exam",
        route: ROUTES.cloudEntryChoice,
        reason: "AWS Cloud Practitioner and AZ-900 are both foundations, so platform direction matters more than their small price difference.",
        nonFit: "A fundamentals exam is not the right next step if you already deploy and operate production cloud resources.",
        credentialRoutes: [ROUTES.awsCloudPractitioner, ROUTES.az900]
      },
      foundation: {
        title: "Compare AWS Cloud Practitioner with AZ-900",
        route: ROUTES.cloudEntryChoice,
        reason: "At the foundation stage, the right public starting point is the platform you can actually use and practice\u2014not a cross-vendor popularity ranking.",
        nonFit: "Skip both when your goal already requires hands-on administration or architecture and you can work with the target platform.",
        credentialRoutes: [ROUTES.awsCloudPractitioner, ROUTES.az900]
      },
      hands_on: {
        title: "Choose between AWS architecture and Azure administration",
        route: ROUTES.cloudHandsOnChoice,
        reason: "Hands-on cloud work makes the role and platform boundary between AWS Solutions Architect Associate and AZ-104 the decision that matters.",
        nonFit: "Do not choose either until the platform and work\u2014architecture versus administration\u2014match the responsibility you want.",
        credentialRoutes: [ROUTES.awsSaa, ROUTES.az104]
      },
      experienced: {
        title: "Use the AWS SAA versus AZ-104 boundary as a scope check",
        route: ROUTES.cloudHandsOnChoice,
        reason: "RoleMath\u2019s strongest current public cloud decision separates architecture from administration, but it does not yet cover every advanced cloud specialty.",
        nonFit: "If both associate-level scopes sit below your work, treat that as a RoleMath coverage gap rather than an instruction to collect another credential.",
        credentialRoutes: [ROUTES.awsSaa, ROUTES.az104]
      }
    }
  };
  function normalizeRoute(route) {
    if (!route.startsWith("/")) return `/${route.replace(/^\/+/, "").replace(/\/+$/, "")}/`;
    return route.endsWith("/") ? route : `${route}/`;
  }
  function routesArePublic(routes, publicRoutes) {
    return routes.every((route) => publicRoutes.has(normalizeRoute(route)));
  }
  function actionFor(definition, priority2, publicRoutes) {
    if (definition.primaryCredentialRoute) {
      const suffix = priority2 === "lowest_cost" ? "total-cost/" : priority2 === "fastest_start" ? "free-study/" : "";
      const candidate = normalizeRoute(`${definition.primaryCredentialRoute}${suffix}`);
      if (suffix && publicRoutes.has(candidate)) {
        return {
          route: candidate,
          label: priority2 === "lowest_cost" ? "See the complete cost first" : "Start with official and free preparation"
        };
      }
    }
    return { route: normalizeRoute(definition.route), label: "Open the decision" };
  }
  function priorityClause(priority2) {
    if (priority2 === "lowest_cost") return "cost matters, but fit still controls the shortlist";
    if (priority2 === "fastest_start") return "the fastest honest start is the smallest step that still matches your background";
    return "role fit takes priority over speed and exam price";
  }
  function prioritizedReason(reason, priority2) {
    return `${reason.replace(/[.!?]+$/, "")}; ${priorityClause(priority2)}.`;
  }
  function plan(targetWork2, experienceStage2, priority2, publicRoutes) {
    const normalizedPublic = new Set([...publicRoutes].map(normalizeRoute));
    if (!targetWork2 || !experienceStage2 || !priority2) {
      return {
        kind: "not_started",
        title: "Choose three answers to see one next decision.",
        route: null,
        reason: "RoleMath will not show a default certification before you describe the work, background, and tradeoff.",
        nonFit: "",
        alternative: null,
        nextActionLabel: null,
        evidenceChecked: CHECKED
      };
    }
    if (targetWork2 === "unsure") {
      return {
        kind: "direction",
        title: "Choose the work before you choose an exam.",
        route: normalizedPublic.has("/certifications/") ? "/certifications/" : null,
        reason: "Support, networking, security, and cloud credentials lead toward different work; an exam-first answer would be arbitrary.",
        nonFit: "Do not buy the cheapest foundation exam just to create momentum\u2014first decide which work you want to test through a small project or lab.",
        alternative: null,
        nextActionLabel: normalizedPublic.has("/certifications/") ? "Compare the four work directions" : null,
        evidenceChecked: CHECKED
      };
    }
    const definition = DECISIONS[targetWork2][experienceStage2];
    if (!definition) {
      const fallbackRoute = normalizedPublic.has("/certifications/") ? "/certifications/" : null;
      return {
        kind: "coverage_gap",
        title: "RoleMath has an advanced-support coverage gap.",
        route: fallbackRoute,
        reason: "RoleMath does not currently have enough reviewed advanced support coverage to recommend a credential for the experience you described.",
        nonFit: "Do not use an entry-support credential as a substitute when your work already includes independent support ownership or leadership.",
        alternative: null,
        nextActionLabel: fallbackRoute ? "Review the published credential coverage" : null,
        evidenceChecked: CHECKED
      };
    }
    if (!normalizedPublic.has(normalizeRoute(definition.route)) || !routesArePublic(definition.credentialRoutes, normalizedPublic)) {
      const fallbackRoute = normalizedPublic.has("/certifications/") ? "/certifications/" : null;
      return {
        kind: "coverage_gap",
        title: "RoleMath does not have a fully public match for this answer.",
        route: fallbackRoute,
        reason: "A decision or credential needed by this result is currently held, so the fit check will not recommend it.",
        nonFit: "Do not substitute a held or partially reviewed credential merely to force a result for this combination.",
        alternative: null,
        nextActionLabel: fallbackRoute ? "Review the published credential coverage" : null,
        evidenceChecked: CHECKED
      };
    }
    const action = actionFor(definition, priority2, normalizedPublic);
    const alternative = definition.alternative && normalizedPublic.has(normalizeRoute(definition.alternative.route)) && routesArePublic(definition.alternative.credentialRoutes, normalizedPublic) ? { ...definition.alternative, route: normalizeRoute(definition.alternative.route) } : null;
    return {
      kind: "recommendation",
      title: definition.title,
      route: action.route,
      reason: prioritizedReason(definition.reason, priority2),
      nonFit: definition.nonFit,
      alternative,
      nextActionLabel: action.label,
      evidenceChecked: CHECKED
    };
  }
  function parseState(params) {
    const one = (key, allowed) => {
      const value = params.get(key);
      return value && allowed.includes(value) ? value : null;
    };
    return {
      targetWork: one("work", TARGET_WORK.map((choice) => choice.value)),
      experienceStage: one("stage", EXPERIENCE_STAGES.map((choice) => choice.value)),
      priority: one("priority", PRIORITIES.map((choice) => choice.value))
    };
  }
  function stateToQuery(targetWork2, experienceStage2, priority2) {
    return `?work=${targetWork2}&stage=${experienceStage2}&priority=${priority2}`;
  }

  // tmp/fit-check-sidecar.ts
  var PUBLIC = /* @__PURE__ */ new Set([
    "/certifications/",
    "/certifications/comptia/comptia-a-plus/",
    "/certifications/comptia/comptia-network-plus/",
    "/certifications/comptia/comptia-network-plus/free-study/",
    "/certifications/comptia/comptia-network-plus/total-cost/",
    "/certifications/cisco/cisco-ccna/",
    "/certifications/cisco/cisco-ccna/free-study/",
    "/certifications/cisco/cisco-ccna/total-cost/",
    "/certifications/isc2/isc2-cc-certified-in-cybersecurity/",
    "/certifications/comptia/comptia-security-plus/",
    "/certifications/isc2/isc2-sscp-systems-security-certified-practitioner/",
    "/certifications/isaca/isaca-cism-certified-information-security-manager/",
    "/certifications/isc2/isc2-cissp-certified-information-systems-security-professional/",
    "/certifications/aws/aws-certified-cloud-practitioner/",
    "/certifications/microsoft/microsoft-az-900/",
    "/certifications/aws/aws-solutions-architect-associate/",
    "/certifications/microsoft/microsoft-az-104/",
    "/compare/comptia-network-plus-vs-cisco-ccna/",
    "/compare/comptia-security-plus-vs-isc2-cc/",
    "/compare/isc2-sscp-vs-comptia-security-plus/",
    "/compare/isaca-cism-vs-isc2-cissp/",
    "/compare/aws-cloud-practitioner-vs-microsoft-azure-fundamentals/",
    "/compare/microsoft-azure-administrator-vs-aws-solutions-architect-associate/"
  ]);
  var targetWork = null;
  var experienceStage = null;
  var priority = null;
  var questions = document.querySelector("#fit-questions");
  var result = document.querySelector("#fit-result");
  if (!questions || !result) throw new Error("Fit Check mount points are missing");
  var parsed = parseState(new URLSearchParams(window.location.search));
  targetWork = parsed.targetWork;
  experienceStage = parsed.experienceStage;
  priority = parsed.priority;
  function escapeHtml(value) {
    return value.replace(/[&<>'"]/g, (character) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      "'": "&#39;",
      '"': "&quot;"
    })[character] ?? character);
  }
  function rolemath(route) {
    return `https://rolemath.com${route}`;
  }
  function choiceGroup(legend, name, choices, selected) {
    return `<fieldset class="choice-group"><legend>${escapeHtml(legend)}</legend><div class="choice-grid">${choices.map(
      (choice) => `<button class="choice" type="button" aria-pressed="${selected === choice.value}" data-name="${name}" data-value="${choice.value}"><strong>${escapeHtml(choice.label)}</strong><span>${escapeHtml(choice.hint)}</span></button>`
    ).join("")}</div></fieldset>`;
  }
  function render() {
    questions.innerHTML = [
      choiceGroup("What work are you targeting?", "work", TARGET_WORK, targetWork),
      choiceGroup("What experience do you already have?", "stage", EXPERIENCE_STAGES, experienceStage),
      choiceGroup("What matters most for this decision?", "priority", PRIORITIES, priority)
    ].join("");
    const outcome = plan(targetWork, experienceStage, priority, PUBLIC);
    if (outcome.kind === "not_started") {
      result.innerHTML = `<p class="eyebrow">No default result</p><h2>Choose all three answers.</h2><p>${escapeHtml(outcome.reason)}</p>`;
      return;
    }
    const action = outcome.route && outcome.nextActionLabel ? `<p><a class="result-cta" href="${rolemath(outcome.route)}">${escapeHtml(outcome.nextActionLabel)} \u2192</a></p>` : "";
    const alternative = outcome.alternative ? `<div class="alternative"><h3>One alternative</h3><p><a href="${rolemath(outcome.alternative.route)}">${escapeHtml(outcome.alternative.title)}</a> \u2014 ${escapeHtml(outcome.alternative.when)}</p></div>` : "";
    result.innerHTML = `<p class="eyebrow">${outcome.kind === "coverage_gap" ? "Coverage gap" : "Your next decision"}</p><h2>${escapeHtml(outcome.title)}</h2><p>${escapeHtml(outcome.reason)}</p><p class="nonfit"><strong>Not the right move when:</strong> ${escapeHtml(outcome.nonFit)}</p>${action}${alternative}<p class="small">Fit logic reviewed ${outcome.evidenceChecked}. Current facts remain on the linked RoleMath page.</p>`;
  }
  questions.addEventListener("click", (event) => {
    const button = event.target.closest("[data-name][data-value]");
    if (!button) return;
    if (button.dataset.name === "work") targetWork = button.dataset.value;
    if (button.dataset.name === "stage") experienceStage = button.dataset.value;
    if (button.dataset.name === "priority") priority = button.dataset.value;
    if (targetWork && experienceStage && priority) {
      window.history.replaceState(null, "", `${window.location.pathname}${stateToQuery(targetWork, experienceStage, priority)}`);
    }
    render();
  });
  render();
})();
