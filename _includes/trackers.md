{%- comment -%}
Live trackers section, shared by index.md and fr/index.md.
Usage: include trackers.md lang="en"   (inside a markdown="1" section)
Text: _data/trackers.yml (one block per language). Live figures: assets/trackers.js.
{%- endcomment -%}
{%- assign t = site.data.trackers[include.lang] -%}
{%- assign us_src = "https://www.genaiadoptiontracker.com/" -%}
{%- assign lift_url = "https://heclift.github.io/website/en/ai-trackers/diffusion-emploi/index.html" -%}
{%- assign lift_src = "https://heclift.github.io/website/data/ai-trackers/diffusion-emploi/offers_total.csv" -%}
{%- assign lift_sum = "https://heclift.github.io/website/data/ai-trackers/diffusion-emploi/general_results.csv" -%}
{{ t.intro }}

### {{ t.h_us }} {#tracker-use-at-work}

{% if t.us_para != "" %}{{ t.us_para }}{% endif %}

<div class="tracker-cards" id="us-cards" data-src="{{ us_src }}">
  <div class="tracker-card"><span class="tracker-value" data-series="any">{{ t.us_values.any }}</span><span class="tracker-label">{{ t.us_card_any }}</span><span class="tracker-delta" data-series="any" data-suffix="{{ t.us_delta }}">{{ t.us_values.d_any }}{{ t.us_delta }}</span></div>
  <div class="tracker-card"><span class="tracker-value" data-series="work">{{ t.us_values.work }}</span><span class="tracker-label">{{ t.us_card_work }}</span><span class="tracker-delta" data-series="work" data-suffix="{{ t.us_delta }}">{{ t.us_values.d_work }}{{ t.us_delta }}</span></div>
  <div class="tracker-card"><span class="tracker-value" data-series="hours">{{ t.us_values.hours }}</span><span class="tracker-label">{{ t.us_card_hours }}</span><span class="tracker-delta" data-series="hours" data-suffix="{{ t.us_delta }}">{{ t.us_values.d_hours }}{{ t.us_delta }}</span></div>
  <div class="tracker-card"><span class="tracker-value" data-series="saved">{{ t.us_values.saved }}</span><span class="tracker-label">{{ t.us_card_saved }}</span><span class="tracker-delta" data-series="saved" data-suffix="{{ t.us_delta }}">{{ t.us_values.d_saved }}{{ t.us_delta }}</span></div>
</div>
<p class="tracker-note" id="us-cards-note" data-live="{{ t.us_note_live | escape }}">{{ t.us_note_static }}</p>
<details class="tracker-fold" id="us-waves" hidden>
  <summary>{{ t.us_details }}</summary>
  <div class="tracker-table"><table>
    <thead><tr>{% for h in t.us_th %}<th scope="col">{{ h }}</th>{% endfor %}</tr></thead>
    <tbody id="us-waves-body"></tbody>
  </table></div>
</details>

{% if t.us_subgroups != "" %}{{ t.us_subgroups }}{% endif %}

{{ t.us_sources }}
{:.tracker-sources}

### {{ t.h_fr }} {#tracker-job-postings}

{{ t.lift_para }}

<div class="tracker-cards" id="lift-cards" data-src="{{ lift_src }}" data-summary="{{ lift_sum }}">
  <div class="tracker-card"><span class="tracker-value" data-key="ai_total">{{ t.lift_values[0] }}</span><span class="tracker-label">{{ t.lift_cards[0] }}</span><span class="tracker-delta" data-key="ai_quarter" data-prefix="+" data-suffix="{{ t.lift_delta }}">+{{ t.lift_deltas[0] }}{{ t.lift_delta }}</span></div>
  <div class="tracker-card"><span class="tracker-value" data-key="genai_total">{{ t.lift_values[1] }}</span><span class="tracker-label">{{ t.lift_cards[1] }}</span><span class="tracker-delta" data-key="genai_quarter" data-prefix="+" data-suffix="{{ t.lift_delta }}">+{{ t.lift_deltas[1] }}{{ t.lift_delta }}</span></div>
  <div class="tracker-card"><span class="tracker-value" data-sum="Number of firms with AI offers">{{ t.lift_values[2] }}</span><span class="tracker-label">{{ t.lift_cards[2] }}</span></div>
  <div class="tracker-card"><span class="tracker-value" data-sum="Number of firms with GenAI offers">{{ t.lift_values[3] }}</span><span class="tracker-label">{{ t.lift_cards[3] }}</span></div>
</div>
<p class="tracker-note" id="lift-cards-note" data-live="{{ t.lift_note_live | escape }}">{{ t.lift_note_static }}</p>

{{ t.lift_trend }}

<details class="tracker-fold">
  <summary>{{ t.lift_details }}</summary>
  <div class="tracker-embed"><iframe src="{{ lift_url }}" title="{{ t.lift_iframe_title | escape }}" loading="lazy" referrerpolicy="no-referrer"></iframe></div>
  <p class="tracker-note">{{ t.lift_embed_note }}</p>
</details>

{{ t.lift_other }}

{{ t.lift_sources }}
{:.tracker-sources}

<script defer src="{{ '/assets/trackers.js' | relative_url }}"></script>
